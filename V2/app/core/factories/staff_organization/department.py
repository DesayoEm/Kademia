from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from ...errors.staff_organisation_errors import DepartmentInUseError
from ....core.errors.user_errors import RelatedStaffNotFoundError
from ....core.validators.staff_organization import StaffOrganizationValidator
from ....core.validators.entity_validators import EntityValidator
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
        self.entity_validator = EntityValidator(session)
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

            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
        )
        try:
            return self.repository.create(department)

        except UniqueViolationError as e:
            error_message = str(e)
            if 'staff_departments_name_key' in error_message:
                raise DuplicateDepartmentError(
                    entry=new_department.name, detail=error_message, field='name'
                )
            raise DuplicateDepartmentError(entry='unknown', detail=str(e), field='unknown')


        except RelationshipError as e:
            raise RelationshipError(error=str(e), operation='create', entity='unknown_entity')


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
            raise DepartmentNotFoundError(identifier=department_id, detail = str(e))


    def get_all_departments(self, filters) -> List[StaffDepartment]:
        """Get all active departments with filtering.
        Returns:
            List[StaffDepartment]: List of active departments
        """
        fields = ['name']
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

            validations = {
                "name": (self.validator.validate_name, "name"),
                "description": (self.validator.validate_name, "description"),
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in data:
                    validated_value = validator_func(data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            existing.last_modified_by = SYSTEM_USER_ID
            return self.repository.update(department_id, existing)

        except EntityNotFoundError as e:
            raise DepartmentNotFoundError(identifier=department_id, detail = str(e))

        except UniqueViolationError as e:
            error_message = str(e)
            if 'staff_departments_name_key' in error_message:
                raise DuplicateDepartmentError(
                    entry=original.get('name', 'unknown'), detail=error_message, field='name'
                )
            raise DuplicateDepartmentError(entry='unknown', detail=str(e), field = 'unknown')

        except RelationshipError as e:
            raise RelationshipError(error=str(e), operation='update', entity='staff')


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
            raise DepartmentNotFoundError(identifier=department_id, detail = str(e))


    def delete_department(self, department_id: UUID) -> None:
        """Permanently delete a staff department.
        Args:
            department_id (UUID): ID of department to delete
        """
        try:
            self.repository.delete(department_id)

        except EntityNotFoundError as e:
            raise DepartmentNotFoundError(identifier=department_id, detail = str(e))

        except RelationshipError as e:
            error_message = str(e)
            # Note: Referenced FKs are SET NULL on delete, so RelationshipError may not trigger here,
            # but it is being kept for unexpected constraint issues.
            raise RelationshipError(error=error_message, operation='delete', entity='unknown_entity')


    def get_all_archived_departments(self, filters) -> List[StaffDepartment]:
        """Get all archived departments with filtering.
        Returns:
            List[StaffDepartment]: List of archived department records
        """
        fields = ['name']
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
            raise DepartmentNotFoundError(identifier=department_id, detail = str(e))


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
            raise DepartmentNotFoundError(identifier=department_id, detail = str(e))


    def delete_archived_department(self, department_id: UUID) -> None:
        """Permanently delete an archived department.
        Args:
            department_id: ID of department to delete
        """
        try:
            self.repository.delete_archive(department_id)
        except EntityNotFoundError as e:
            raise DepartmentNotFoundError(identifier=department_id, detail = str(e))

        except RelationshipError as e:
            error_message = str(e)
            # Note: Referenced FKs are SET NULL on delete, so RelationshipError may not trigger here,
            # but it is being kept for unexpected constraint issues.
            raise RelationshipError(error=error_message, operation='delete', entity='unknown_entity')
