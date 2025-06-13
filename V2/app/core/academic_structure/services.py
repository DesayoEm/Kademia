from sqlalchemy import func, select
from sqlalchemy.orm import Session
from uuid import UUID
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.academic_structure.validators import AcademicStructureValidator
from V2.app.core.academic_structure.models.academic_structure import AcademicLevel, Classes, StudentDepartment


class AcademicStructureService:
    def __init__(self, session: Session):
        self.level_repository = SQLAlchemyRepository(AcademicLevel, session)
        self.class_repository = SQLAlchemyRepository(Classes, session)
        self.validator = AcademicStructureValidator()
        self.export_service = ExportService(session)


    def return_default_level_order(self) -> int:
        """Create a new order value by getting the max order + 1 for the given level"""
        stmt = (
            select(func.max(AcademicLevel.display_order))
        )
        result = self.level_repository.session.execute(stmt).scalar_one_or_none()
        return 1 if result is None else result + 1


    def create_class_order(self, level_id: UUID) -> int:
        """Create a new order value by getting the max order + 1 for the given level"""

        stmt = (
            select(func.max(Classes.order))
            .where(Classes.level_id == level_id)
        )
        result = self.class_repository.session.execute(stmt).scalar_one_or_none()
        return 1 if result is None else result + 1


    def export_academic_level(self, level_id: UUID, export_format: str) -> str:
        """Export academic level and its associated data
        Args:
            level_id: level UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            AcademicLevel, level_id, export_format
        )

    def export_class(self, class_id: UUID, export_format: str) -> str:
        """Export class and its associated data
        Args:
            class_id: level UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Classes, class_id, export_format
        )

    def export_department(self, department_id: UUID, export_format: str) -> str:
        """Export department and its associated data
        Args:
            department_id: level UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            StudentDepartment, department_id, export_format
        )
