from ...database.models.enums import ArchiveReason
from ...schemas.staff_organization.department import (
    StaffDepartmentCreate, StaffDepartmentUpdate, StaffDepartmentResponse, DepartmentFilterParams
)
from ...core.factories.staff_organization.department import StaffDepartmentFactory
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List


class StaffDepartmentCrud:
    """CRUD operations for staff departments."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        self.factory = StaffDepartmentFactory(session)


    def create_department(self, data: StaffDepartmentCreate) -> StaffDepartmentResponse:
        """Create a new department.
        Args:
            data: Validated department creation data
        Returns:
            StaffDepartmentResponse: Created department
        """
        department = self.factory.create_staff_department(data)
        return StaffDepartmentResponse.model_validate(department)


    def get_department(self, department_id: UUID) -> StaffDepartmentResponse:
        """Get department by ID.
        Args:
            department_id: Department UUID
        Returns:
            StaffDepartmentResponse: Retrieved department
        """
        department = self.factory.get_staff_department(department_id)
        return StaffDepartmentResponse.model_validate(department)


    def get_all_departments(self, filters: DepartmentFilterParams) -> List[StaffDepartmentResponse]:
        """Get all active departments.
        Returns:
            List[StaffDepartmentResponse]: List of active departments
        """
        departments = self.factory.get_all_departments(filters)
        return [StaffDepartmentResponse.model_validate(department) for department in departments]


    def update_department(self, department_id: UUID, data: StaffDepartmentUpdate) -> StaffDepartmentResponse:
        """Update department information.
        Args:
            department_id: Department UUID
            data: Validated update data
        Returns:
            StaffDepartmentResponse: Updated department
        """
        data = data.model_dump()
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


    def delete_department(self, department_id: UUID) -> None:
        """Permanently delete a department.
        Args:
            department_id: Department UUID
        """
        self.factory.delete_department(department_id)



    # Archived department operations
    def get_archived_department(self, department_id: UUID) -> StaffDepartmentResponse:
        """Get an archived department by ID.
        Args:
            department_id: department UUID
        Returns:
            StaffDepartmentResponse: Retrieved archived department
        """
        department = self.factory.get_archived_department(department_id)
        return StaffDepartmentResponse.model_validate(department)

    def get_all_archived_departments(self, filters: DepartmentFilterParams) -> List[StaffDepartmentResponse]:
        """Get all archived departments.
        Args:
            filters: Filter parameters
        Returns:
            List[StaffDepartmentResponse]: List of archived departments
        """
        departments = self.factory.get_all_archived_departments(filters)
        return [StaffDepartmentResponse.model_validate(department) for department in departments]

    def restore_department(self, department_id: UUID) -> StaffDepartmentResponse:
        """Restore an archived department.
        Args:
            department_id: department UUID
        Returns:
            StaffDepartmentResponse: Restored department
        """
        department = self.factory.restore_department(department_id)
        return StaffDepartmentResponse.model_validate(department)


    def delete_archived_department(self, department_id: UUID) -> None:
        """Permanently delete an archived department.
        Args:
            department_id: department UUID
        """
        self.factory.delete_archived_department(department_id)