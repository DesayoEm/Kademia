from uuid import UUID
from sqlalchemy import text
from sqlalchemy.orm import Session
from ...errors.archive_delete_errors import CascadeDeletionError
from ...errors.database_errors import EntityInUseError, NullFKConstraintMisconfiguredError
from ...errors.error_map import error_map
from .dependency_config import DEPENDENCY_CONFIG
from ....config import config
from ..export_service.export import ExportService
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository


class DeleteService:
    """
    Service for managing entity deletion with various strategies based on entity relationships.

    Provides methods for safely deleting entities with dependency checking, cascading deletion
    for parent-child relationships, and nullify-references deletion for shared entities.

    Attributes:
        session (Session): SQLAlchemy database session
        model: SQLAlchemy model class for the entity
        export_service (ExportService): Service for exporting entities before deletion
        repository (SQLAlchemyRepository): Repository for database operations
    """


    def __init__(self, model, session: Session):
        """
        Initialize the deletion service with a model and database session.

        Args:
            model: SQLAlchemy model class for the entity
            session (Session): SQLAlchemy database session
        """
        self.session = session
        self.model = model
        self.export_service = ExportService(session)
        self.repository = SQLAlchemyRepository(model, session)
        self.anonymous_user = UUID(config.ANONYMIZED_ID)


    @staticmethod
    def check_dependent_entities(entity, entity_model):
        """
        Check if the entity has active related entities that depend on it.

        Examines all configured dependency relationships to see if any references
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


    def safe_delete(self, entity_model, entity_id: UUID, is_archived):
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
                raise EntityInUseError(entity_model=entity_model, dependencies=", ".join(dependent_fields),
                    display_name=display_name, detail=""
                    )



    def cascade_deletion(self, entity, relationship_names: list):
        """
        Cascade delete related entities first, then delete the main entity.

        Used for true parent-child relationships where child entities shouldn't
        exist without their parent. Requires the entity to be exported first.

        Args:
            entity: The entity instance to delete
            relationship_names (list): Names of relationship attributes to cascade delete

        Raises:
            CascadeDeletionError: If the entity hasn't been exported or if deletion fails
        """
        try:
            with self.session.begin():
                if not entity.is_exported:
                    raise CascadeDeletionError(error="Entity not exported before attempted deletion")

                for relationship_name in relationship_names:
                    related = getattr(entity, relationship_name, None)

                    if related is None:
                        continue

                    if isinstance(related, list):
                        for item in related:
                            if item is not None:
                                self.repository.delete(item)
                    else:
                        self.repository.delete(related)

                self.repository.delete(entity)

        except Exception as e:
            raise CascadeDeletionError(error=str(e))


    def export_and_cascade_delete(self, entity_model, entity_id: UUID,
                                  export_format: str, is_archived) -> str:
        """
        Export the entity, then force delete it and all its related entities.

        Used for true parent-child relationships where all related entities
        should be deleted along with the parent. Performs export for record-keeping
        before deletion.

        Args:
            entity_model: SQLAlchemy model class for the entity
            entity_id (UUID): Unique identifier of the entity to delete
            export_format (str): Format for export (pdf, csv, excel)
            is_archived: Whether to check archived or active entities

        Returns:
            str: Path to the exported file

        Raises:
            EntityNotFoundError: If the entity doesn't exist
            CascadeDeletionError: If deletion fails
        """
        relationship_names = [
            relationship_name for relationship_name, _, _, _ in DEPENDENCY_CONFIG.get(entity_model)
        ]

        export_path = self.export_service.export_entity(entity_model, entity_id, export_format)

        entity = (self.repository.get_archive_by_id(entity_id) if is_archived
                  else self.repository.get_by_id(entity_id))
        entity.is_exported = True
        self.cascade_deletion(entity, relationship_names)

        return export_path


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


    def export_and_null_delete(self, entity_model, entity_id: UUID,
                               export_format: str, is_archived) -> str:
        """
        Export the entity, verify foreign key constraints, then delete the entity.

        Used for shared entities where references should be nullified rather than
        cascaded. Verifies that all foreign key constraints are set to ON DELETE SET NULL
        before proceeding with deletion.

        Args:
            entity_model: SQLAlchemy model class for the entity
            entity_id (UUID): Unique identifier of the entity to delete
            export_format (str): Format for export (pdf, csv, excel)
            is_archived: Whether to check archived or active entities

        Returns:
            str: Path to the exported file

        Raises:
            ForeignKeyConstraintMisconfiguredError: If foreign keys aren't set to ON DELETE SET NULL
            EntityNotFoundError: If the entity doesn't exist
        """

        table_name = entity_model.__tablename__
        fk_rules = self.get_fk_delete_rules_from_info_schema(table_name)

        error_info = error_map.get(entity_model)
        _, display_name = error_info

        for fk_name, rule in fk_rules.items():
            if rule != 'SET NULL':
                raise NullFKConstraintMisconfiguredError(
                        fk_name=fk_name, entity_model=entity_model, display_name=display_name,
                    )

        export_path = self.export_service.export_entity(entity_model, entity_id, export_format)
        entity = (self.repository.get_archive_by_id(entity_id) if is_archived
                  else self.repository.get_by_id(entity_id))

        entity.is_exported = True

        return export_path