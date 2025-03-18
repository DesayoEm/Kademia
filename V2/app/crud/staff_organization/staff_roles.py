from ...database.models.data_enums import ArchiveReason
from ...schemas.staff_organization.staff_roles import (
    StaffRoleCreate, StaffRoleUpdate, StaffRoleResponse, RolesFilterParams
)
from ...core.factories.staff_organization.role import StaffRolesFactory
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List


class StaffRoleCrud:
    """CRUD operations for staff roles, including active and archived entities."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        self.factory = StaffRolesFactory(session)

    # Active role operations
    def create_role(self, data: StaffRoleCreate) -> StaffRoleResponse:
        """Create a new staff role.
        Args:
            data: Validated role creation data
        Returns:
            StaffRoleResponse: Created role
        """
        role = self.factory.create_role(data)
        return StaffRoleResponse.model_validate(role)


    def get_role(self, role_id: UUID) -> StaffRoleResponse:
        """Get a staff role by ID.
        Args:
            role_id: Role UUID
        Returns:
            StaffRoleResponse: Retrieved role
        """
        role = self.factory.get_role(role_id)
        return StaffRoleResponse.model_validate(role)


    def get_all_roles(self, filters: RolesFilterParams) -> List[StaffRoleResponse]:
        """Get all active staff roles.
        Args:
            filters: Filter parameters
        Returns:
            List[StaffRoleResponse]: List of active roles
        """
        roles = self.factory.get_all_roles(filters)
        return [StaffRoleResponse.model_validate(role) for role in roles]


    def update_role(self, role_id: UUID, data: StaffRoleUpdate) -> StaffRoleResponse:
        """Update a staff role.
        Args:
            role_id: Role UUID
            data: Validated update data
        Returns:
            StaffRoleResponse: Updated role
        """
        data = data.model_dump()
        updated_role = self.factory.update_role(role_id, data)
        return StaffRoleResponse.model_validate(updated_role)

    def archive_role(self, role_id: UUID, reason: ArchiveReason) -> None:
        """Archive a staff role.
        Args:
            role_id: Role UUID
            reason: Reason for archiving
        Returns:
            StaffRoleResponse: Archived role
        """
        self.factory.archive_role(role_id, reason)



    def delete_role(self, role_id: UUID) -> None:
        """Permanently delete a staff role.
        Args:
            role_id: Role UUID
        """
        self.factory.delete_role(role_id)

    # Archived role operations
    def get_archived_role(self, role_id: UUID) -> StaffRoleResponse:
        """Get an archived staff role by ID.
        Args:
            role_id: Role UUID
        Returns:
            StaffRoleResponse: Retrieved archived role
        """
        role = self.factory.get_archived_role(role_id)
        return StaffRoleResponse.model_validate(role)

    def get_all_archived_roles(self, filters: RolesFilterParams) -> List[StaffRoleResponse]:
        """Get all archived staff roles.
        Args:
            filters: Filter parameters
        Returns:
            List[StaffRoleResponse]: List of archived roles
        """
        roles = self.factory.get_all_archived_roles(filters)
        return [StaffRoleResponse.model_validate(role) for role in roles]

    def restore_role(self, role_id: UUID) -> StaffRoleResponse:
        """Restore an archived staff role.
        Args:
            role_id: Role UUID
        Returns:
            StaffRoleResponse: Restored role
        """
        role = self.factory.restore_role(role_id)
        return StaffRoleResponse.model_validate(role)


    def delete_archived_role(self, role_id: UUID) -> None:
        """Permanently delete an archived staff role.
        Args:
            role_id: Role UUID
        """
        self.factory.delete_archived_role(role_id)