from sqlalchemy import func, select
from uuid import UUID
from sqlalchemy.orm import Session
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....core.validators.student_organization import StudentOrganizationValidator
from ....database.models.student_organization import AcademicLevel

class AcademicLevelService:
    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(AcademicLevel, session)
        self.validator = StudentOrganizationValidator()

    def create_order(self, level_id: UUID) -> int:
        """Create a new order value by getting the max order + 1 for the given level"""
        stmt = (
            select(func.max(AcademicLevel.order))
            .where(AcademicLevel.id == level_id)
        )
        result = self.repository.session.execute(stmt).scalar_one_or_none()
        return 1 if result is None else result + 1