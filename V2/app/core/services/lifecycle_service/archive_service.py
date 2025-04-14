from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from V2.app.core.services.lifecycle_service.dependency_config import DEPENDENCY_CONFIG


class ArchiveService:
    """
    Service for managing entity archival and checking dependencies before archival.

    Provides methods to check if an entity can be safely archived by
    verifying that no active entities are referencing it.

    Attributes:
        session (Session): SQLAlchemy database session
    """

    def __init__(self, session: Session):
        """
        Initialize the archive service with a database session.

        Args:
            session (Session): SQLAlchemy database session
        """
        self.session = session

    def check_active_dependencies_exists(
            self, entity_model, target_id: UUID,
            is_archived_field: str = "is_archived") -> List[str]:
        """
        Check if any active entities are referencing the target entity.

        Examines all configured dependency relationships to see if any active
        (non-archived) entities reference the target entity, which would prevent
        safe archival.

        Args:
            entity_model: SQLAlchemy model class for the entity type being checked
            target_id (UUID): The ID of the entity to check for dependencies
            is_archived_field (str): The field name used to determine if an entity is archived

        Returns:
            List[str]: Display names of entity types that have active dependencies
                       on the target entity. Empty list if no dependencies exist.
        """
        dependencies = DEPENDENCY_CONFIG.get(entity_model)
        failed = []

        for relationship_title, model_class, fk_field, display_name in dependencies:
            table = model_class.__table__

            conditions = [table.c[fk_field] == target_id,
                          table.c[is_archived_field] == False]

            stmt = select(exists().where(*conditions))
            if self.session.execute(stmt).scalar_one():
                failed.append(display_name)

        return failed