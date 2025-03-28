from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from ....core.errors.user_profile_errors import RelatedStaffNotFoundError
from ....core.validators.staff_organization import StaffOrganizationValidator
from ....database.models.staff_organization import StaffDepartment
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....database.models.enums import ArchiveReason
from ....core.errors.database_errors import EntityNotFoundError, UniqueViolationError, RelationshipError
from ....core.errors.staff_organisation_errors import DepartmentNotFoundError, DuplicateDepartmentError


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class StaffDepartmentFactory:
    """Factory class for managing staff department operations."""

    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(StaffDepartment, session)
        self.validator = StaffOrganizationValidator()

    def create_staff_department(self, new_department) -> StaffDepartment:
        """Create a new staff department.
        Args:
            new_department: Department data containing name and description
        Returns:
            StaffDepartment: Created department record
        """
        department = StaffDepartment(
            id=uuid4(),
            name=self.validator.validate_name(new_department.name),
            description=self.validator.validate_name(new_department.description),
            manager_id=new_department.manager_id,
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
        )
        try:
            return self.repository.create(department)
        except UniqueViolationError as e:
            raise DuplicateDepartmentError(
                input_value=new_department.name, detail=str(e), field = 'name'
            )
        except RelationshipError as e:
            error_message = str(e)
            fk_error_mapping = {
                'fk_staff_departments_staff_manager_id': ('manager_id', RelatedStaffNotFoundError),
            }
            for fk_constraint, (attr_name, error_class) in fk_error_mapping.items():
                if fk_constraint in error_message:
                    entity_id = getattr(new_department, attr_name, None)
                    if entity_id:
                        raise error_class(id=entity_id, detail=error_message, action='create')
            raise RelationshipError(error=error_message, operation='create', entity='unknown_entity')


    def get_staff_department(self, department_id: UUID) -> StaffDepartment:
        """Get a specific staff department by ID.
        Args:
            department_id (UUID): ID of department to retrieve
        Returns:
            StaffDepartment: Retrieved department record
        """
        try:
            return self.repository.get_by_id(department_id)
        except EntityNotFoundError as e:
            raise DepartmentNotFoundError(id=department_id, detail = str(e))


    def get_all_departments(self, filters) -> List[StaffDepartment]:
        """Get all active departments with filtering.
        Returns:
            List[StaffDepartment]: List of active departments
        """
        fields = ['name', 'description']
        return self.repository.execute_query(fields, filters)


    def update_staff_department(self, department_id: UUID, data: dict) -> StaffDepartment:
        """Update a staff department's information.
        Args:
            department_id (UUID): ID of department to update
            data (dict): Dictionary containing fields to update
        Returns:
            StaffDepartment: Updated department record
        """
        original = data.copy()
        try:
            existing = self.get_staff_department(department_id)
            if 'name' in data:
                existing.name = self.validator.validate_name(data.pop('name'))
            if 'description' in data:
                existing.description = self.validator.validate_name(data.pop('description'))
            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            existing.last_modified_by = SYSTEM_USER_ID #Placeholder

            return self.repository.update(department_id, existing)
        except EntityNotFoundError as e:
            raise DepartmentNotFoundError(id=department_id, detail = str(e))
        except UniqueViolationError as e:
            raise DuplicateDepartmentError(#name is the only field with a unique constraint
                input_value=original.get('name', 'unknown'), detail=str(e), field = 'name'
            )
        except RelationshipError as e:
            error_message = str(e)
            fk_error_mapping = {
                'fk_staff_departments_staff_manager_id': ('manager_id', RelatedStaffNotFoundError),
            }
            for fk_constraint, (attr_name, error_class) in fk_error_mapping.items():
                if fk_constraint in error_message:
                    entity_id = data.get(attr_name, None)
                    if entity_id:
                        raise error_class(id=entity_id, detail=error_message, action='update')
            raise RelationshipError(error=error_message, operation='update', entity='unknown_entity')


    def archive_department(self, department_id: UUID, reason: ArchiveReason) -> StaffDepartment:
        """Archive a staff department.
        Args:
            department_id (UUID): ID of department to archive
            reason (ArchiveReason): Reason for archiving
        Returns:
            StaffDepartment: Archived department record
        """
        try:
            return self.repository.archive(department_id, SYSTEM_USER_ID, reason)
        except EntityNotFoundError as e:
            raise DepartmentNotFoundError(id=department_id, detail = str(e))


    def delete_department(self, department_id: UUID) -> None:
        """Permanently delete a staff department.
        Args:
            department_id (UUID): ID of department to delete
        """
        try:
            self.repository.delete(department_id)
        except EntityNotFoundError as e:
            raise DepartmentNotFoundError(id=department_id, detail = str(e))


    def get_all_archived_departments(self, filters) -> List[StaffDepartment]:
        """Get all archived departments with filtering.
        Returns:
            List[StaffDepartment]: List of archived department records
        """
        fields = ['name', 'description']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_department(self, department_id: UUID) -> StaffDepartment:
        """Get an archived department by ID.
        Args:
            department_id: ID of department to retrieve
        Returns:
            StaffDepartment: Retrieved department record
        """
        try:
            return self.repository.get_archive_by_id(department_id)
        except EntityNotFoundError as e:
            raise DepartmentNotFoundError(id=department_id, detail = str(e))

    def restore_department(self, department_id: UUID) -> StaffDepartment:
        """Restore an archived department.
        Args:
            department_id: ID of department to restore
        Returns:
            StaffDepartment: Restored department record
        """
        try:
            archived = self.get_archived_department(department_id)
            archived.last_modified_by = SYSTEM_USER_ID
            return self.repository.restore(department_id)
        except EntityNotFoundError as e:
            raise DepartmentNotFoundError(id=department_id, detail = str(e))


    def delete_archived_department(self, department_id: UUID) -> None:
        """Permanently delete an archived department.
        Args:
            department_id: ID of department to delete
        """
        try:
            self.repository.delete_archive(department_id)
        except EntityNotFoundError as e:
            raise DepartmentNotFoundError(id=department_id, detail = str(e))