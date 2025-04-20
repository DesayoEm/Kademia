from sqlalchemy import func, select
from uuid import UUID
from sqlalchemy.orm import Session

from V2.app.core.shared.database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.academic_structure.validators.academic_structure import AcademicStructureValidator
from V2.app.core.academic_structure.models.academic_structure import Classes


class ClassService:
    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(Classes, session)
        self.validator = AcademicStructureValidator()

    def create_order(self, level_id: UUID) -> int:
        """Create a new order value by getting the max order + 1 for the given level"""

        stmt = (
            select(func.max(Classes.order))
            .where(Classes.level_id == level_id)
        )
        result = self.repository.session.execute(stmt).scalar_one_or_none()
        return 1 if result is None else result + 1