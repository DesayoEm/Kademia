from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.academic_structure.models.academic_structure import StudentDepartment
from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.academic_structure.schemas.department import (
    DepartmentCreate, DepartmentUpdate, DepartmentResponse, DepartmentFilterParams
)
from V2.app.core.academic_structure.factories.department import StudentDepartmentFactory
from V2.app.core.shared.services.export_service.export import ExportService


class DepartmentCrud:
    """CRUD operations for student departments."""

    def __init__(self, session: Session, current_user = None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.current_user = current_user
        self.factory = StudentDepartmentFactory(session, current_user = current_user)
        self.export_service = ExportService(session)


    def create_department(self, data: DepartmentCreate) -> DepartmentResponse:
        """Create a new department."""
        department = self.factory.create_student_department(data)
        return DepartmentResponse.model_validate(department)


    def get_department(self, department_id: UUID) -> DepartmentResponse:
        """Get department by ID."""
        department = self.factory.get_student_department(department_id)
        return DepartmentResponse.model_validate(department)


    def get_all_departments(self, filters: DepartmentFilterParams) -> List[DepartmentResponse]:
        """Get all active departments."""
        departments = self.factory.get_all_student_departments(filters)
        return [DepartmentResponse.model_validate(department) for department in departments]


    def update_department(self, department_id: UUID, data: DepartmentUpdate) -> DepartmentResponse:
        """Update department information."""
        data = data.model_dump(exclude_unset=True)
        updated_department = self.factory.update_student_department(department_id, data)
        return DepartmentResponse.model_validate(updated_department)


    def archive_department(self, department_id: UUID, reason: ArchiveReason) -> None:
        """Archive a department.
        Args:
            department_id: Department UUID
            reason: Reason for archiving
        Returns:
            DepartmentResponse: Archived department
        """
        self.factory.archive_student_department(department_id, reason)


    def export_department(self, department_id: UUID, export_format: str) -> str:
        """Export department and its associated data
        Args:
            department_id: Department UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            StudentDepartment, department_id, export_format
        )


    def delete_department(self, department_id: UUID) -> None:
        """Permanently delete a department."""
        self.factory.delete_student_department(department_id)


    # Archived department operations
    def get_archived_department(self, department_id: UUID) -> DepartmentResponse:
        """Get an archived department by ID."""
        department = self.factory.get_archived_department(department_id)
        return DepartmentResponse.model_validate(department)


    def get_all_archived_departments(self, filters: DepartmentFilterParams) -> List[DepartmentResponse]:
        """Get all archived departments."""
        departments = self.factory.get_all_archived_departments(filters)
        return [DepartmentResponse.model_validate(department) for department in departments]


    def restore_department(self, department_id: UUID) -> DepartmentResponse:
        """Restore an archived department."""
        department = self.factory.restore_department(department_id)
        return DepartmentResponse.model_validate(department)


    def delete_archived_department(self, department_id: UUID) -> None:
        """Permanently delete an archived department."""
        self.factory.delete_archived_department(department_id)