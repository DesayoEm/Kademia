from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.shared.exceptions import EntityInUseError
from app.core.shared.exceptions.maps.error_map import error_map
from app.infra.settings import config
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from .dependency_config import DEPENDENCY_CONFIG

class DeleteService:
    """
    Service for managing entity deletion with various strategies based on entity relationships.

    Methods are for safely deleting entities with dependency checking, cascading deletion
    for parent-child relationships, and nullify-references deletion for shared entities.

    Attributes:
        session (Session): SQLAlchemy db session
        model: SQLAlchemy model class for the entity
        repository (SQLAlchemyRepository): Repository for db operations
    """

    def __init__(self, model, session: Session):
        """
        Initialize the deletion service with a model and db session.
        Args:
            model: SQLAlchemy model class for the entity
            session (Session): SQLAlchemy db session
        """
        self.session = session
        self.model = model
        self.repository = SQLAlchemyRepository(model, session)
        self.anonymous_user = UUID(config.ANONYMIZED_ID)


    @staticmethod
    def check_dependent_entities(entity, entity_model):
        """
        Check if the entity has active related entities that depend on it.

        Examines configured dependency relationships to see if any references
        to this entity exist, which would prevent safe deletion.

        Args:
            entity: The entity instance to check
            entity_model: The SQLAlchemy model class of the entity

        Returns:
            list: Names of dependent entity types that reference this entity
        """
        dependencies = DEPENDENCY_CONFIG.get(entity_model)
        dependent_fields = []

        for relationship_title, model_class, fk_field, display_name in dependencies:
            related = getattr(entity, relationship_title, None)

            if related:
                if isinstance(related, list) and len(related) > 0:
                    dependent_fields.append(display_name)
                elif related is not None:
                    dependent_fields.append(display_name)

        return dependent_fields


    def check_safe_delete(self, entity_model, entity_id: UUID, is_archived):
        """
        Safely delete an entity only if no dependent entities exist.

        Checks for any active references to this entity and raises an appropriate
        error if dependencies exist, preventing accidental deletion of referenced entities.

        Args:
            entity_model: SQLAlchemy model class for the entity
            entity_id (UUID): Unique identifier of the entity to delete
            is_archived: Whether to check archived or active entities

        Raises:
            DeletionDependencyError: If active dependencies exist that prevent deletion
            EntityNotFoundError: If the entity doesn't exist
        """

        entity = (self.repository.get_archive_by_id(entity_id) if is_archived
                  else self.repository.get_by_id(entity_id))

        error_info = error_map.get(entity_model)
        _, display_name = error_info

        dependent_fields = self.check_dependent_entities(entity, entity_model)

        if dependent_fields:
                raise EntityInUseError(
                    entity_model=entity_model, dependencies=", ".join(dependent_fields),
                    display_name=display_name,
                    detail="Could not safely delete"
            )


    def get_fk_delete_rules_from_info_schema(self, table_name: str) -> dict:
        """
        Returns a mapping of FK constraint names to their delete rules
        for a given table using information_schema.

        Args:
            table_name (str): Name of the table to inspect

        Returns:
            dict: Mapping {constraint_name: delete_rule}
        """
        query = text("""
               SELECT
                   tc.constraint_name,
                   rc.delete_rule
               FROM
                   information_schema.table_constraints tc
               JOIN
                   information_schema.referential_constraints rc
                   ON tc.constraint_name = rc.constraint_name
               WHERE
                   tc.constraint_type = 'FOREIGN KEY'
                   AND tc.table_name = :table_name
           """)
        result = self.session.execute(query, {'table_name': table_name}).fetchall()
        return {row.constraint_name: row.delete_rule.upper() for row in result}


