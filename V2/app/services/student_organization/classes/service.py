from sqlalchemy import func
from uuid import UUID
from sqlalchemy.orm import Session
from ....database.db_repositories.sqlalchemy_repos.main_repo import SQLAlchemyRepository
from ....services.student_organization.validators import StudentOrganizationValidators
from ....database.models.student_organization import Classes

class ClassFactoryService:
    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(Classes, session)
        self.validator = StudentOrganizationValidators()

    def create_order(self, level_id: UUID) -> int:
        """Create a new order value by getting the max order + 1 for the given level"""
        max_order = self.repository.session.query(func.max(Classes.order)) \
            .filter(Classes.level_id == level_id) \
            .scalar()

        return 1 if not max_order else max_order + 1