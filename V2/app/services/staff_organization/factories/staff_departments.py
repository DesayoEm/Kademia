from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from ....services.staff_organization.validators import StaffOrganizationValidators
from ....database.models.staff_organization import StaffDepartments
from ....database.db_repositories.sqlalchemy_repos.main_repo import SQLAlchemyRepository
from ....database.models.data_enums import ArchiveReason
from ....services.errors.database_errors import EntityNotFoundError, UniqueViolationError
from ....services.errors.staff_organisation_errors import DepartmentNotFoundError, DuplicateDepartmentError


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class StaffDepartmentsFactory:
    """Factory class for managing staff department operations."""

    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(StaffDepartments, session)
        self.validator = StaffOrganizationValidators()

    def create_staff_department(self, new_department) -> StaffDepartments:
        """Create a new staff department.
        Args:
            new_department: Department data containing name and description
        Returns:
            StaffDepartments: Created department record
        """
        department = StaffDepartments(
            id=uuid4(),
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
            name=self.validator.validate_name(new_department.name),
            description=self.validator.validate_name(new_department.description),
            manager_id=new_department.manager_id
        )
        try:
            return self.repository.create(department)
        except UniqueViolationError as e:
            raise DuplicateDepartmentError(input=new_department.name, original_error=e)


    def get_all_departments(self, filters) -> List[StaffDepartments]:
        """Get all active departments with filtering.
        Returns:
            List[StaffDepartments]: List of active departments
        """
        fields = ['name', 'description']
        return self.repository.execute_query(fields, filters)


    def get_staff_department(self, department_id: UUID) -> StaffDepartments:
        """Get a specific staff department by ID.
        Args:
            department_id (UUID): ID of department to retrieve
        Returns:
            StaffDepartments: Retrieved department record
        """
        try:
            return self.repository.get_by_id(department_id)
        except EntityNotFoundError:
            raise DepartmentNotFoundError(id=department_id)


    def update_staff_department(self, department_id: UUID, data: dict) -> StaffDepartments:
        """Update a staff department's information.
        Args:
            department_id (UUID): ID of department to update
            data (dict): Dictionary containing fields to update
        Returns:
            StaffDepartments: Updated department record
        """
        try:
            existing = self.get_staff_department(department_id)
            if 'name' in data:
                existing.name = self.validator.validate_name(data['name'])
            if 'description' in data:
                existing.description = self.validator.validate_name(data['description'])
            existing.last_modified_by = SYSTEM_USER_ID

            return self.repository.update(department_id, existing)
        except EntityNotFoundError:
            raise DepartmentNotFoundError(id=department_id)
        except UniqueViolationError as e:
            field_name = getattr(e, 'field_name', 'name')
            field_value = data.get(field_name, '')
            raise DuplicateDepartmentError(input=field_value, original_error=e)


    def archive_department(self, department_id: UUID, reason: ArchiveReason) -> StaffDepartments:
        """Archive a staff department.
        Args:
            department_id (UUID): ID of department to archive
            reason (ArchiveReason): Reason for archiving
        Returns:
            StaffDepartments: Archived department record
        """
        try:
            return self.repository.archive(department_id, SYSTEM_USER_ID, reason)
        except EntityNotFoundError:
            raise DepartmentNotFoundError(id=department_id)


    def delete_department(self, department_id: UUID) -> None:
        """Permanently delete a staff department.
        Args:
            department_id (UUID): ID of department to delete
        """
        try:
            self.repository.delete(department_id)
        except EntityNotFoundError:
            raise DepartmentNotFoundError(id=department_id)


    def get_all_archived_departments(self, filters) -> List[StaffDepartments]:
        """Get all archived departments with filtering.
        Returns:
            List[StaffDepartments]: List of archived department records
        """
        fields = ['name', 'description']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_department(self, department_id: UUID) -> StaffDepartments:
        """Get an archived department by ID.
        Args:
            department_id: ID of department to retrieve
        Returns:
            StaffDepartments: Retrieved department record
        """
        try:
            return self.repository.get_archive_by_id(department_id)
        except EntityNotFoundError:
            raise DepartmentNotFoundError(id=department_id)

    def restore_department(self, department_id: UUID) -> StaffDepartments:
        """Restore an archived department.
        Args:
            department_id: ID of department to restore
        Returns:
            StaffDepartments: Restored department record
        """
        try:
            archived = self.get_archived_department(department_id)
            archived.last_modified_by = SYSTEM_USER_ID
            return self.repository.restore(department_id)
        except EntityNotFoundError:
            raise DepartmentNotFoundError(id=department_id)


    def delete_archived_department(self, department_id: UUID) -> None:
        """Permanently delete an archived department.
        Args:
            department_id: ID of department to delete
        """
        try:
            self.repository.delete_archive(department_id)
        except EntityNotFoundError:
            raise DepartmentNotFoundError(id=department_id)