from sqlalchemy import func, select
from sqlalchemy.orm import Session

from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.academic_structure.validators.academic_structure import AcademicStructureValidator
from V2.app.core.academic_structure.models.academic_structure import AcademicLevel


class AcademicLevelService:
    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(AcademicLevel, session)
        self.validator = AcademicStructureValidator()

    def return_default_order(self) -> int:
        """Create a new order value by getting the max order + 1 for the given level"""
        stmt = (
            select(func.max(AcademicLevel.order))
        )
        result = self.repository.session.execute(stmt).scalar_one_or_none()
        return 1 if result is None else result + 1