from sqlalchemy import func
from uuid import UUID
from sqlalchemy.orm import Session
from V2.app.database.db_repositories.sqlalchemy_repos.main_repo import SQLAlchemyRepository
from V2.app.core.validators.student_organization import StudentOrganizationValidators
from V2.app.database.models.student_organization import AcademicLevel

class AcademicLevelService:
    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(AcademicLevel, session)
        self.validator = StudentOrganizationValidators()

    def create_order(self, level_id: UUID) -> int:
        """Create a new order value by getting the max order + 1 for the given level"""
        max_order = self.repository.session.query(
            func.max(AcademicLevel.order)
            ).filter(AcademicLevel.id == level_id).scalar()

        return 1 if not max_order else max_order + 1