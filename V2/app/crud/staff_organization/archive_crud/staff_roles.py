from ....schemas.staff_organization.staff_roles import (
     StaffRoleResponse, RolesFilterParams
)
from ....services.staff_organization.archive_factories.staff_roles import ArchiveStaffRolesFactory
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
        self.factory = ArchiveStaffRolesFactory(session)


    def get_archived_role(self, role_id: UUID) -> StaffRoleResponse:
        """Get an archived staff role by ID.
        Args:
            role_id: Role UUID
        Returns:
            StaffRoleResponse: Retrieved role
        """
        role = self.factory.get_archived_role(role_id)
        return StaffRoleResponse.model_validate(role)

    def get_all_archived_roles(self, filters: RolesFilterParams) -> List[StaffRoleResponse]:
        """Get all archived staff roles.
        Returns:
            List[StaffRoleResponse]: List of archived roles
        """
        roles = self.factory.get_all_archived_roles(filters)
        return [StaffRoleResponse.model_validate(role) for role in roles]


    def restore_role(self, role_id: UUID) -> StaffRoleResponse:
        """Restore a staff role.
        Args:
            role_id: Role UUID
        Returns:
            StaffRoleResponse: Restored role
        """
        role = self.factory.restore_role(role_id)
        return StaffRoleResponse.model_validate(role)


    def delete_role(self, role_id: UUID) -> None:
        """Permanently delete a staff role.
        Args:
            role_id: Role UUID
        """
        self.factory.delete_role(role_id)