from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from ...errors.staff_organisation_errors import RoleArchivalDependencyError
from ...services.export_service.export import ExportService
from ...services.lifecycle_service.archive_service import ArchiveService
from ....core.validators.staff_organization import StaffOrganizationValidator
from ....database.models.staff_organization import StaffRole
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....database.models.enums import ArchiveReason
from ....core.errors.database_errors import EntityNotFoundError, UniqueViolationError
from ....core.errors.staff_organisation_errors import RoleNotFoundError, DuplicateRoleError


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class StaffRoleFactory:
    """Factory class for managing staff role operations."""

    def __init__(self, session: Session):
        """Initialize factory with database session.
        Args:
            session: SQLAlchemy database session
        """
        self.repository = SQLAlchemyRepository(StaffRole, session)
        self.validator = StaffOrganizationValidator()
        self.archive_helper = ArchiveService(session)
        self.export = ExportService(session)


    def create_role(self, new_role) -> StaffRole:
        """Create a new staff role.
        Args:
            new_role: Role data containing name and description
        Returns:
            StaffRole: Created role record
        """
        role = StaffRole(
            id=uuid4(),
            name=self.validator.validate_name(new_role.name),
            description=self.validator.validate_description(new_role.description),
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
        )
        try:
            return self.repository.create(role)

        except UniqueViolationError as e:
            error_message= str(e)
            if 'staff_roles_name_key' in error_message:
                raise DuplicateRoleError(
                    entry=new_role.name, detail=error_message, field = 'name'
                )
            raise DuplicateRoleError(entry='unknown', detail=error_message, field='unknown')


    def get_all_roles(self, filters) -> List[StaffRole]:
        """Get all active staff roles with filtering.
        Returns:
            List[StaffRole]: List of active role records
        """
        fields = ['name']
        return self.repository.execute_query(fields, filters)


    def get_role(self, role_id: UUID) -> StaffRole:
        """Get a specific staff role by id.
        Args:
            role_id: id of role to retrieve
        Returns:
            StaffRole: Retrieved role record
        """
        try:
            return self.repository.get_by_id(role_id)
        except EntityNotFoundError as e:
            raise RoleNotFoundError(identifier=role_id, detail = str(e))


    def update_role(self, role_id: UUID, data: dict) -> StaffRole:
        """Update a staff role's information.
        Args:
            role_id: id of role to update
            data: Dictionary containing fields to update
        Returns:
            StaffRole: Updated role record
        """
        original = data.copy()

        try:
            existing = self.get_role(role_id)
            validations = {
                "name": (self.validator.validate_name, "name"),
                "description": (self.validator.validate_description, "description"),
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in data:
                    validated_value = validator_func(data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(role_id, existing)

        except EntityNotFoundError as e:
            raise RoleNotFoundError(identifier=role_id, detail = str(e))

        except UniqueViolationError as e:
            error_message = str(e)
            if 'staff_roles_name_key' in error_message:
                raise DuplicateRoleError(
                    entry=original.get('name', 'unknown'), detail=str(e), field = 'name'
                )

            raise DuplicateRoleError(entry='unknown', detail=error_message, field='unknown')


    def archive_role(self, role_id: UUID, reason: ArchiveReason) -> StaffRole:
        """Archive a role if no active staff members are assigned to it.
        Args:
            role_id: id of role to archive
            reason: Reason for archiving
        Returns:
            StaffRole: Archived role record
        """
        try:
            failed_dependencies = self.archive_helper.check_active_dependencies_exists(
                entity_type=StaffRole,
                target_id=role_id
            )

            if failed_dependencies:
                raise RoleArchivalDependencyError(
                    entity_name=", ".join(failed_dependencies),
                    identifier=str(role_id)
                )

            return self.repository.archive(role_id, SYSTEM_USER_ID, reason)

        except EntityNotFoundError as e:
            raise RoleNotFoundError(identifier=role_id, detail = str(e))


    def delete_role(self, role_id: UUID) -> None:
        """Permanently delete a staff role.
        Args:
            role_id: id of role to delete
        """
        try:
            self.repository.delete(role_id)
        except EntityNotFoundError as e :
            raise RoleNotFoundError(identifier=role_id, detail = str(e))


    def get_all_archived_roles(self, filters) -> List[StaffRole]:
        """Get all archived staff roles with filtering.
        Returns:
            List[StaffRole]: List of archived role records
        """
        fields = ['name']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_role(self, role_id: UUID) -> StaffRole:
        """Get an archived role by ID.
        Args:
            role_id: id of role to retrieve
        Returns:
            StaffRole: Retrieved role record
        """
        try:
            return self.repository.get_archive_by_id(role_id)
        except EntityNotFoundError as e:
            raise RoleNotFoundError(identifier=role_id, detail = str(e))

    def restore_role(self, role_id: UUID) -> StaffRole:
        """Restore an archived role.
        Args:
            role_id: id of role to restore
        Returns:
            StaffRole: Restored role record
        """
        try:
            archived = self.get_archived_role(role_id)
            archived.last_modified_by = SYSTEM_USER_ID
            return self.repository.restore(role_id)
        except EntityNotFoundError as e:
            raise RoleNotFoundError(identifier=role_id, detail = str(e))


    def delete_archived_role(self, role_id: UUID) -> None:
        """Permanently delete an archived role.
        Args:
            role_id: id of role to delete
        """
        try:
            self.repository.delete_archive(role_id)
        except EntityNotFoundError as e:
            raise RoleNotFoundError(identifier=role_id, detail = str(e))

