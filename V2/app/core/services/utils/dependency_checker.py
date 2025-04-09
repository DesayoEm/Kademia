from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from typing import Type, Optional, List, Tuple
from uuid import UUID

class DependencyChecker:
    def __init__(self, session: Session):
        self.session = session

    def check_active_dependencies_exists(
        self,
        dependencies: List[Tuple[Type, str]],
        target_id: UUID,
        is_archived_field: str,
        check_active_only: bool = False,
    ) -> List[str]:
        """
        Check multiple dependencies for a given entity.

        Args:
            dependencies (List[Tuple[Model, ForeignKeyField]]): List of (model, field) pairs
            target_id (UUID): The ID to check against
            is_archived_field (str): Field name to filter by active status
            check_active_only (bool): Only consider non-archived (active) entities

        Returns:
            List[str]: List of model names where active dependencies exist
        """
        failed = []
        for dependent_model, fk_field in dependencies:
            conditions = [getattr(dependent_model, fk_field) == target_id]

            if check_active_only and hasattr(dependent_model, is_archived_field):
                conditions.append(getattr(dependent_model, is_archived_field) == False)

            stmt = select(exists().where(*conditions))
            if self.session.execute(stmt).scalar_one():
                failed.append(dependent_model.__tablename__)

        return failed


