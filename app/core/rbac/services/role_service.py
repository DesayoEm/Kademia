from uuid import UUID
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from typing import List
from app.core.shared.exceptions import EntityNotFoundError
from app.core.shared.exceptions.auth_errors import SameRoleError
from app.core.shared.exceptions import NoMatchingRoleError
from app.core.shared.models.enums import UserRoleName
from app.core.rbac.models import Role, Permission


class RBACService:
    """
    Service for role-based access control operations.

    Provides business logic for RBAC including role lookups, permission
    retrieval, and validation of role changes. Used by factories and
    other services that need to work with roles and permissions.

    Attributes:
        session: SQLAlchemy database session.
    """
    def __init__(self, session: Session):
        """
        Initialize the RBACService with a database session.

        Args:
            session: An active SQLAlchemy Session instance for database operations.
        """
        self.session = session

    @staticmethod
    def prevent_redundant_changes(current_role_id: UUID, new_role_id: UUID) -> UUID:
        """
        Validate that a role change is actually changing the role.

        Prevents creating unnecessary role history records when the "new" role
        is the same as the current role.

        Args:
            current_role_id: The user's current role UUID.
            new_role_id: The proposed new role UUID.

        Returns:
            UUID: The new_role_id if it differs from current_role_id.

        Raises:
            SameRoleError: If current_role_id equals new_role_id.
        """
        if current_role_id == new_role_id:
            raise SameRoleError(previous=current_role_id, new=new_role_id)

        return new_role_id


    def fetch_role_id(self, role_name: str) -> UUID:
        """
        Look up a role's UUID by its name.

        Converts a role name string to the corresponding UserRoleName enum
        and retrieves the role's UUID from the database.

        Args:
            role_name: The role name as a string (must match a UserRoleName
                enum member, e.g., "ADMIN", "TEACHER").

        Returns:
            UUID: The role's primary key.

        Raises:
            KeyError: If role_name doesn't match any UserRoleName enum member.
            NoMatchingRoleError: If no role exists in the database with the
                given name.

        """
        try:
            stmt = select(Role).where(Role.name == UserRoleName[role_name])
            role_obj = self.session.execute(stmt).scalar_one()
            role_id = role_obj.id
            return role_id

        except NoResultFound as e:
            raise NoMatchingRoleError(role_name, str(e))


    def get_role_permission_strs(self, role_id: UUID) -> List[str]:
        """
        Get all permission names assigned to a role.

        Eagerly loads the role's permissions and returns their names as strings.
        Useful for authorization checks and permission displays.

        Args:
            role_id: The UUID of the role to get permissions for.

        Returns:
            List[str]: List of permission name strings (e.g., ["view_students",
                "edit_grades", "manage_classes"]).

        Raises:
            EntityNotFoundError: If no role exists with the given ID.

        Note:
            Uses selectinload to eagerly fetch permissions in a single query,
            avoiding N+1 query issues.
        """

        role = (
            self.session.query(Role)
            .options(selectinload(Role.permissions))
            .filter(Role.id == role_id)
            .first()
        )
        if not role:
            raise EntityNotFoundError(Role, role_id, "Role not found", "role")

        permissions = role.permissions
        return [permission.name for permission in permissions]
