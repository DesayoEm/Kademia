from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from ....database.db_repositories.sqlalchemy_repos.main_repo import SQLAlchemyRepository
from ....database.models.data_enums import ArchiveReason
from ....services.errors.database_errors import EntityNotFoundError, UniqueViolationError
from ....services.student_organization.validators import StudentOrganizationValidators
from ....database.models.student_organization import StudentDepartments
from ....services.errors.student_organisation_error import (
     DuplicateStudentDepartmentError, StudentDepartmentNotFoundError
    )

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class StudentDepartmentsFactory:
    """Factory class for managing student department operations."""
    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(StudentDepartments, session)
        self.validator = StudentOrganizationValidators()

    def create_student_department(self, new_department) -> StudentDepartments:
        """Create a new student department.
        Args:
            new_department: Department data containing name and description
        Returns:
            StudentDepartments: Created department record
        """
        department = StudentDepartments(
            id = uuid4(),
            name = self.validator.validate_name(new_department.name),
            description = self.validator.validate_name(new_department.description),
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID
        )
        try:
            return self.repository.create(department)
        except UniqueViolationError as e:
            raise DuplicateStudentDepartmentError(input=new_department.name, original_error=e)

    def get_student_department(self, department_id: UUID) -> StudentDepartments:
        """Get a specific student department by ID.
        Args:
            department_id (UUID): ID of department to retrieve
        Returns:
            StudentDepartments: Retrieved department record
        """
        try:
            return self.repository.get_by_id(department_id)
        except EntityNotFoundError:
            raise StudentDepartmentNotFoundError(id=department_id)


    def get_all_departments(self, filters) -> List[StudentDepartments]:
        """Get all active departments with filtering.
        Returns:
            List[StudentDepartments]: List of active departments
        """
        fields = ['name', 'description']
        return self.repository.execute_query(fields, filters)

    def update_student_department(self, department_id: UUID, data: dict) -> StudentDepartments:
        """Update a student department's information.
        Args:
            department_id (UUID): ID of department to update
            data (dict): Dictionary containing fields to update
        Returns:
            StudentDepartments: Updated department record
        """
        try:
            existing = self.get_student_department(department_id)
            if 'name' in data:
                existing.name = self.validator.validate_name(data['name'])
            if 'description' in data:
                existing.description = self.validator.validate_name(data['description'])
            existing.last_modified_by = SYSTEM_USER_ID

            return self.repository.update(department_id, existing)
        except EntityNotFoundError:
            raise StudentDepartmentNotFoundError(id=department_id)
        except UniqueViolationError as e:
            field_name = getattr(e, 'field_name', 'name or department')
            field_value = data.get(field_name, '')
            raise DuplicateStudentDepartmentError(input=field_value, original_error=e)


    def archive_department(self, department_id: UUID, reason: ArchiveReason) -> StudentDepartments:
        """Archive a student department.
        Args:
            department_id (UUID): ID of department to archive
            reason (ArchiveReason): Reason for archiving
        Returns:
            StudentDepartments: Archived department record
        """
        try:
            return self.repository.archive(department_id, SYSTEM_USER_ID, reason)
        except EntityNotFoundError:
            raise StudentDepartmentNotFoundError(id=department_id)


    def delete_department(self, department_id: UUID) -> None:
        """Permanently delete a student department.
        Args:
            department_id (UUID): ID of department to delete
        """
        try:
            self.repository.delete(department_id)
        except EntityNotFoundError:
            raise StudentDepartmentNotFoundError(id=department_id)


    def get_all_archived_departments(self, filters) -> List[StudentDepartments]:
        """Get all archived departments with filtering.
        Returns:
            List[StudentDepartments]: List of archived department records
        """
        fields = ['name', 'description']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_department(self, department_id: UUID) -> StudentDepartments:
        """Get an archived department by ID.
        Args:
            department_id: ID of department to retrieve
        Returns:
            StudentDepartments: Retrieved department record
        """
        try:
            return self.repository.get_archive_by_id(department_id)
        except EntityNotFoundError:
            raise StudentDepartmentNotFoundError(id=department_id)

    def restore_department(self, department_id: UUID) -> StudentDepartments:
        """Restore an archived department.
        Args:
            department_id: ID of department to restore
        Returns:
            StudentDepartments: Restored department record
        """
        try:
            archived = self.get_archived_department(department_id)
            archived.last_modified_by = SYSTEM_USER_ID
            return self.repository.restore(department_id)
        except EntityNotFoundError:
            raise StudentDepartmentNotFoundError(id=department_id)


    def delete_archived_department(self, department_id: UUID) -> None:
        """Permanently delete an archived department.
        Args:
            department_id: ID of department to delete
        """
        try:
            self.repository.delete_archive(department_id)
        except EntityNotFoundError:
            raise StudentDepartmentNotFoundError(id=department_id)

