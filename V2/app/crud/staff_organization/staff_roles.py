from ...database.models.data_enums import ArchiveReason
from ...schemas.staff_organization.staff_roles import (
    StaffRoleCreate, StaffRoleUpdate, StaffRoleResponse
)
from ...services.staff_organization.factories.staff_roles import StaffRolesFactory
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List


class StaffRoleCrud:
    """CRUD operations for staff roles."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        self.factory = StaffRolesFactory(session)


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


    def get_all_roles(self) -> List[StaffRoleResponse]:
        """Get all active staff roles.
        Returns:
            List[StaffRoleResponse]: List of active roles
        """
        roles = self.factory.get_all_roles()
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

    def archive_role(self, role_id: UUID, reason: ArchiveReason) -> StaffRoleResponse:
        """Archive a staff role.
        Args:
            role_id: Role UUID
            reason: Reason for archiving
        Returns:
            StaffRoleResponse: Archived role
        """
        role = self.factory.archive_role(role_id, reason)
        return StaffRoleResponse.model_validate(role)


    def delete_role(self, role_id: UUID) -> None:
        """Permanently delete a staff role.
        Args:
            role_id: Role UUID
        """
        self.factory.delete_role(role_id)