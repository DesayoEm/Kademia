from sqlalchemy import func, select
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.shared.validators.entity_validators import EntityValidator
from app.core.academic_structure.factories.classes import ClassFactory
from app.core.academic_structure.factories.academic_level import AcademicLevelFactory
from app.core.academic_structure.factories.department import StudentDepartmentFactory
from app.core.shared.services.audit_export_service.export import ExportService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.academic_structure.services.validators import AcademicStructureValidator
from app.core.academic_structure.models import AcademicLevel, Classes, StudentDepartment


class AcademicStructureService:
    def __init__(self, session: Session, current_user=None):

        self.class_factory = ClassFactory(session, current_user=current_user)
        self.level_factory = AcademicLevelFactory(session, current_user=current_user)
        self.department_factory = StudentDepartmentFactory(session, current_user=current_user)

        self.level_repository = SQLAlchemyRepository(AcademicLevel, session)
        self.class_repository = SQLAlchemyRepository(Classes, session)
        self.entity_validator = EntityValidator(session)
        self.validator = AcademicStructureValidator()
        self.export_service = ExportService(session)

    def return_default_level_order(self) -> int:
        """Create a new order value by getting the max order + 1 for the given level"""
        stmt = select(func.max(AcademicLevel.display_order))
        result = self.level_repository.session.execute(stmt).scalar_one_or_none()
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


    # Class Management
    def create_class_order(self, level_id: UUID) -> int:
        """Create a new order value by getting the max order + 1 for the given level"""
        stmt = (
            select(func.max(Classes.order))
            .where(Classes.level_id == level_id)
        )
        result = self.class_repository.session.execute(stmt).scalar_one_or_none()
        return 1 if result is None else result + 1


    def assign_class_supervisor(self, class_id: UUID, supervisor_id: UUID | None = None):
        """Assign a supervisor to a class"""

        if not supervisor_id:
            return self.class_factory.update_class(
                class_id, {"supervisor_id": None}
            )

        #Validate supervisor exists before updating due to polymorphic association
        validated_supervisor_id = self.entity_validator.validate_staff_exists(supervisor_id)

        return self.class_factory.update_class(
            class_id, {"supervisor_id": validated_supervisor_id}
        )


    def assign_class_student_rep(self, class_id: UUID, rep_id: UUID | None = None):
        """Assign a student representative to a class"""

        return self.class_factory.update_class(
            class_id, {"student_rep_id": rep_id}
        )

    def assign_class_assistant_rep(self, class_id: UUID, asst_rep_id: UUID | None = None):
        """Assign an assistant representative to a class"""

        return self.class_factory.update_class(
            class_id, {"assistant_rep_id": asst_rep_id}
        )

    def export_class(self, class_id: UUID, export_format: str) -> str:
        """Export class and its associated data
        Args:
            class_id: class UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Classes, class_id, export_format
        )

    # Department Management
    def assign_department_mentor(self, department_id: UUID, mentor_id: UUID | None = None):
        """Assign a mentor to a department"""

        if not mentor_id:
            return self.department_factory.update_student_department(
                department_id, {"mentor_id": None}
            )

        #Validate mentor exists before updating due to polymorphic association
        validated_mentor_id = self.entity_validator.validate_staff_exists(mentor_id)

        return self.department_factory.update_student_department(
            department_id, {"mentor_id": validated_mentor_id}
        )


    def assign_department_student_rep(self, department_id: UUID, rep_id: UUID | None = None):
        """Assign a student representative to a department"""

        return self.department_factory.update_student_department(
            department_id, {"student_rep_id": rep_id}
        )

    def assign_department_assistant_rep(self, department_id: UUID, asst_rep_id: UUID | None = None):
        """Assign an assistant representative to a department"""

        return self.department_factory.update_student_department(
            department_id, {"assistant_rep_id": asst_rep_id}
        )

    def export_department(self, department_id: UUID, export_format: str) -> str:
        """Export department and its associated data
        Args:
            department_id: department UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            StudentDepartment, department_id, export_format
        )

