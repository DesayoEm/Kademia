from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from ....services.staff_organization.validators import StaffOrganizationValidators
from ....database.models.staff_organization import StaffRoles
from ....database.db_repositories.sqlalchemy_repos.main_repo import SQLAlchemyRepository
from ....database.models.data_enums import ArchiveReason
from ....services.errors.database_errors import EntityNotFoundError, UniqueViolationError
from ....services.errors.staff_organisation_errors import RoleNotFoundError, DuplicateRoleError


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class StaffRolesFactory:
    """Factory class for managing staff role operations."""

    def __init__(self, session: Session):
        """Initialize factory with database session.
        Args:
            session: SQLAlchemy database session
        """
        self.repository = SQLAlchemyRepository(StaffRoles, session)
        self.validator = StaffOrganizationValidators()

    def create_role(self, new_role) -> StaffRoles:
        """Create a new staff role.
        Args:
            new_role: Role data containing name and description
        Returns:
            StaffRoles: Created role record
        """
        role = StaffRoles(
            id=uuid4(),
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
            name=self.validator.validate_name(new_role.name),
            description=self.validator.validate_name(new_role.description)
        )
        try:
            return self.repository.create(role)
        except UniqueViolationError as e:
            raise DuplicateRoleError(name=new_role.name, original_error=e)

    def get_all_roles(self, filters) -> List[StaffRoles]:
        """Get all active staff roles with filtering.
        Returns:
            List[StaffRoles]: List of active role records
        """
        fields = ['name', 'description']
        return self.repository.execute_query(fields, filters)


    def get_role(self, role_id: UUID) -> StaffRoles:
        """Get a specific staff role by ID.
        Args:
            role_id: ID of role to retrieve
        Returns:
            StaffRoles: Retrieved role record
        """
        try:
            return self.repository.get_by_id(role_id)
        except EntityNotFoundError:
            raise RoleNotFoundError(id=role_id)


    def update_role(self, role_id: UUID, data: dict) -> StaffRoles:
        """Update a staff role's information.
        Args:
            role_id: ID of role to update
            data: Dictionary containing fields to update
        Returns:
            StaffRoles: Updated role record
        """
        try:
            existing = self.get_role(role_id)
            if 'name' in data:
                existing.name = self.validator.validate_name(data['name'])
            if 'description' in data:
                existing.description = self.validator.validate_name(data['description'])
            existing.last_modified_by = SYSTEM_USER_ID

            return self.repository.update(role_id, existing)
        except EntityNotFoundError:
            raise RoleNotFoundError(id=role_id)
        except UniqueViolationError as e:
            field_name = getattr(e, 'field_name', 'name')
            field_value = data.get(field_name, '')
            raise DuplicateRoleError(name=field_value, original_error=e)


    def archive_role(self, role_id: UUID, reason: ArchiveReason) -> StaffRoles:
        """Archive a role.
        Args:
            role_id: ID of role to archive
            reason: Reason for archiving
        Returns:
            StaffRoles: Archived role record
        """
        try:
            return self.repository.archive(role_id, SYSTEM_USER_ID, reason)
        except EntityNotFoundError:
            raise RoleNotFoundError(id=role_id)


    def delete_role(self, role_id: UUID) -> None:
        """Permanently delete a staff role.
        Args:
            role_id: ID of role to delete
        """
        try:
            self.repository.delete(role_id)
        except EntityNotFoundError:
            raise RoleNotFoundError(id=role_id)