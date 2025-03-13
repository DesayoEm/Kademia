from ...database.models.data_enums import ArchiveReason
from ...schemas.student_organization.student_departments import (
    DepartmentCreate, DepartmentUpdate, DepartmentResponse, DepartmentFilterParams
)
from ...services.student_organization.factories.student_departments import StudentDepartmentsFactory
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List


class DepartmentCrud:
    """CRUD operations for student departments."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        self.factory = StudentDepartmentsFactory(session)


    def create_department(self, data: DepartmentCreate) -> DepartmentResponse:
        """Create a new department.
        Args:
            data: Validated department creation data
        Returns:
            DepartmentResponse: Created department
        """
        department = self.factory.create_student_department(data)
        return DepartmentResponse.model_validate(department)


    def get_department(self, department_id: UUID) -> DepartmentResponse:
        """Get department by ID.
        Args:
            department_id: Department UUID
        Returns:
            DepartmentResponse: Retrieved department
        """
        department = self.factory.get_student_department(department_id)
        return DepartmentResponse.model_validate(department)


    def get_all_departments(self, filters: DepartmentFilterParams) -> List[DepartmentResponse]:
        """Get all active educator qualifications.
        Returns:
            List[QualificationResponse]: List of active qualifications
        """
        departments = self.factory.get_all_departments(filters)
        return [DepartmentResponse.model_validate(department) for department in departments]


    def update_department(self, department_id: UUID, data: DepartmentUpdate) -> DepartmentResponse:
        """Update department information.
        Args:
            department_id: Department UUID
            data: Validated update data
        Returns:
            DepartmentResponse: Updated department
        """
        data = data.model_dump()
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
        self.factory.archive_department(department_id, reason)


    def delete_department(self, department_id: UUID) -> None:
        """Permanently delete a department.
        Args:
            department_id: Department UUID
        """
        self.factory.delete_department(department_id)


    # Archived department operations
    def get_archived_department(self, department_id: UUID) -> DepartmentResponse:
        """Get an archived department by ID.
        Args:
            department_id: department UUID
        Returns:
            DepartmentResponse: Retrieved archived department
        """
        department = self.factory.get_archived_department(department_id)
        return DepartmentResponse.model_validate(department)

    def get_all_archived_departments(self, filters: DepartmentFilterParams) -> List[DepartmentResponse]:
        """Get all archived departments.
        Args:
            filters: Filter parameters
        Returns:
            List[DepartmentResponse]: List of archived departments
        """
        departments = self.factory.get_all_archived_departments(filters)
        return [DepartmentResponse.model_validate(department) for department in departments]

    def restore_department(self, department_id: UUID) -> DepartmentResponse:
        """Restore an archived department.
        Args:
            department_id: department UUID
        Returns:
            DepartmentResponse: Restored department
        """
        department = self.factory.restore_department(department_id)
        return DepartmentResponse.model_validate(department)


    def delete_archived_department(self, department_id: UUID) -> None:
        """Permanently delete an archived department.
        Args:
            department_id: department UUID
        """
        self.factory.delete_archived_department(department_id)