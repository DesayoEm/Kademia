from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.staff_management.models.staff_management import StaffDepartment
from V2.app.core.staff_management.factories.department import StaffDepartmentFactory
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.staff_management.schemas.department import (
    StaffDepartmentCreate, StaffDepartmentUpdate, StaffDepartmentResponse, DepartmentFilterParams
)

class StaffDepartmentCrud:
    """CRUD operations for staff departments."""

    def __init__(self, session: Session, current_user = None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
        """
        self.session = session
        self.current_user = current_user
        self.factory = StaffDepartmentFactory(session, current_user=current_user)
        self.export_service = ExportService(session)


    def create_department(self, data: StaffDepartmentCreate) -> StaffDepartmentResponse:
        """Create a new department."""
        department = self.factory.create_staff_department(data)
        return StaffDepartmentResponse.model_validate(department)


    def get_department(self, department_id: UUID) -> StaffDepartmentResponse:
        """Get department by ID."""
        department = self.factory.get_staff_department(department_id)
        return StaffDepartmentResponse.model_validate(department)


    def get_all_departments(self, filters: DepartmentFilterParams) -> List[StaffDepartmentResponse]:
        """Get all active departments."""
        departments = self.factory.get_all_departments(filters)
        return [StaffDepartmentResponse.model_validate(department) for department in departments]


    def update_department(self, department_id: UUID, data: StaffDepartmentUpdate) -> StaffDepartmentResponse:
        """Update department information"""
        data = data.model_dump(exclude_unset=True)
        updated_department = self.factory.update_staff_department(department_id, data)
        return StaffDepartmentResponse.model_validate(updated_department)


    def archive_department(self, department_id: UUID, reason: ArchiveReason) -> None:
        """Archive a department.
        Args:
            department_id: Department UUID
            reason: Reason for archiving
        Returns:
            StaffDepartmentResponse: Archived department
        """
        self.factory.archive_department(department_id, reason)


    def export_department(self, department_id: UUID, export_format: str) -> str:
        """Export department and its associated data
        Args:
            department_id: level UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            StaffDepartment, department_id, export_format
        )


    def delete_department(self, department_id: UUID) -> None:
        """Permanently delete a department."""
        self.factory.delete_department(department_id)



    # Archived department operations
    def get_archived_department(self, department_id: UUID) -> StaffDepartmentResponse:
        """Get an archived department by ID."""
        department = self.factory.get_archived_department(department_id)
        return StaffDepartmentResponse.model_validate(department)


    def get_all_archived_departments(self, filters: DepartmentFilterParams) -> List[StaffDepartmentResponse]:
        """Get all archived departments."""
        departments = self.factory.get_all_archived_departments(filters)
        return [StaffDepartmentResponse.model_validate(department) for department in departments]


    def restore_department(self, department_id: UUID) -> StaffDepartmentResponse:
        """Restore an archived department."""
        department = self.factory.restore_department(department_id)
        return StaffDepartmentResponse.model_validate(department)


    def delete_archived_department(self, department_id: UUID) -> None:
        """Permanently delete an archived department."""
        self.factory.delete_archived_department(department_id)