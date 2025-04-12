from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from ...factories.dependency_config import DEPENDENCY_CONFIG



class ArchiveService:
    def __init__(self, session: Session):
        self.session = session

    def check_active_dependencies_exists(
            self,
            entity_type,
            target_id: UUID,
            is_archived_field: str = "is_archived"
    ) -> List[str]:

        """
        Check active dependencies for a given entity.

        Args:
            entity_type: Model:
            target_id (UUID): The ID to check against
            is_archived_field (str): Field name to filter by active status

        Returns:
            List[str]: List of display names where active dependencies exist
        """

        dependencies = DEPENDENCY_CONFIG.get(entity_type)

        failed = []

        for dependent_model, fk_field, display_name in dependencies:
            conditions = [getattr(dependent_model, fk_field) == target_id]

            if hasattr(dependent_model, is_archived_field):
                conditions.append(getattr(dependent_model, is_archived_field) == False)

            stmt = select(exists().where(*conditions))
            if self.session.execute(stmt).scalar_one():
                failed.append(display_name)

        return failed



