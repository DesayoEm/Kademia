from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from ...errors.profile_errors import RelatedEducatorNotFoundError
from ....core.errors.profile_errors import RelatedStudentNotFoundError
from ....database.db_repositories.sqlalchemy_repos.main_repo import SQLAlchemyRepository
from ....database.models.data_enums import ArchiveReason
from ....core.errors.database_errors import EntityNotFoundError, UniqueViolationError, RelationshipError
from ....core.validators.student_organization import StudentOrganizationValidators
from ....database.models.student_organization import StudentDepartments
from ....core.errors.student_organisation_errors import (
     DuplicateStudentDepartmentError, StudentDepartmentNotFoundError
    )

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class StudentDepartmentFactory:
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
            student_rep_id = new_department.student_rep_id,
            assistant_rep_id = new_department.assistant_rep_id,
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID
        )
        try:
            return self.repository.create(department)
        except UniqueViolationError as e:
            error_message = str(e).lower()
            if "student_departments_name_key" in error_message:
                raise DuplicateStudentDepartmentError(
                    input_value=new_department.name, detail=str(e), field = 'name'
                )
            else:
                raise DuplicateStudentDepartmentError(
                    input_value="unknown field", field="unknown", detail=error_message)
        except RelationshipError as e:
            error_message = str(e)
            fk_error_mapping = {
                'student_rep_id': RelatedStudentNotFoundError,
                'assistant_rep_id': RelatedStudentNotFoundError,
                }
            for field, error_class in fk_error_mapping.items():
                if field in error_message:
                    if hasattr(new_department, field):
                        entity_id = getattr(new_department, field)
                        raise error_class(id=entity_id, detail=str(e), action='create')
                    else:
                        raise RelationshipError(error=str(e), operation='create', entity='unknown')



    def get_student_department(self, department_id: UUID) -> StudentDepartments:
        """Get a specific student department by ID.
        Args:
            department_id (UUID): ID of department to retrieve
        Returns:
            StudentDepartments: Retrieved department record
        """
        try:
            return self.repository.get_by_id(department_id)
        except EntityNotFoundError as e:
            raise StudentDepartmentNotFoundError(id=department_id, detail=str(e))


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
        original = data.copy()
        try:
            existing = self.get_student_department(department_id)
            if 'name' in data:
                existing.name = self.validator.validate_name(data.pop('name'))
            if 'description' in data:
                existing.description = self.validator.validate_name(data.pop('description'))
            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.last_modified_by = SYSTEM_USER_ID

            return self.repository.update(department_id, existing)
        except EntityNotFoundError as e:
            raise StudentDepartmentNotFoundError(id=department_id, detail=str(e))
        except UniqueViolationError as e:
            raise DuplicateStudentDepartmentError(
                input_value=original.get('name', 'unknown'), detail=str(e), field='name')
        except RelationshipError as e:
            error_message = str(e)
            fk_error_mapping = {
                'student_rep_id': RelatedStudentNotFoundError,
                'assistant_rep_id': RelatedStudentNotFoundError,
                'mentor_id': RelatedEducatorNotFoundError,
            }
            for field, error_class in fk_error_mapping.items():
                if field in error_message:
                    if field in data:
                        entity_id = data[field]
                        raise error_class(id=entity_id, detail=str(e), action='update')
            raise RelationshipError(error=str(e), operation='update', entity='unknown')


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
        except EntityNotFoundError as e:
            raise StudentDepartmentNotFoundError(id=department_id, detail=str(e))

    def delete_department(self, department_id: UUID) -> None:
        """Permanently delete a student department.
        Args:
            department_id (UUID): ID of department to delete
        """
        try:
            self.repository.delete(department_id)
        except EntityNotFoundError as e:
            raise StudentDepartmentNotFoundError(id=department_id, detail=str(e))


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
        except EntityNotFoundError as e:
            raise StudentDepartmentNotFoundError(id=department_id, detail=str(e))

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
        except EntityNotFoundError as e:
            raise StudentDepartmentNotFoundError(id=department_id, detail=str(e))

    def delete_archived_department(self, department_id: UUID) -> None:
        """Permanently delete an archived department.
        Args:
            department_id: ID of department to delete
        """
        try:
            self.repository.delete_archive(department_id)
        except EntityNotFoundError as e:
            raise StudentDepartmentNotFoundError(id=department_id, detail=str(e))
