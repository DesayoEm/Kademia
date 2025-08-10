from uuid import UUID
from typing import List
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy import select, exists
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



    def check_active_dependencies_exists(
            self, entity_model, target_id: UUID) -> List[str]:
        """
        Check if any active entities are referencing the target entity using DEPENDENCY CONFIG
        Args:
            entity_model: SQLAlchemy model class for the entity type being checked
            target_id (UUID): The ID of the entity to check for dependencies

        Returns:
            List[str]: Display names of entity types that have active dependencies
                       on the target entity. Empty list if no dependencies exist.
        """
        dependencies = DEPENDENCY_CONFIG.get(entity_model)
        failed = []

        for _, model_class, fk_field, display_name in dependencies:
            #fk based check
            table = model_class.__table__
            stmt = select(exists().where(table.c[fk_field] == target_id,
               ))

            if self.session.execute(stmt).scalar_one():
                failed.append(display_name)

        return failed


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


