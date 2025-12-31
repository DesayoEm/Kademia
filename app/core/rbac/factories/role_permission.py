from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.core.rbac.models import RolePermission
from app.core.rbac.services.utils import RBACUtils
from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.validators.entity_validators import EntityValidator
from app.core.shared.validators.entry_validators import EntryValidator
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_unique_violation import (
    resolve_unique_violation,
)
from app.core.shared.exceptions.decorators.resolve_fk_violation import (
    resolve_fk_on_create,
    resolve_fk_on_update,
    resolve_fk_on_delete,
)
from app.core.shared.exceptions import EntityNotFoundError
from app.core.shared.exceptions.maps.error_map import error_map


class RolePermissionFactory(BaseFactory):
    """
    Factory for managing role-permission assignments.

    Handles the many-to-many relationship between roles and permissions,
    allowing permissions to be granted to or revoked from roles. Unlike
    other factories, RolePermission uses a composite primary key (role_id,
    permission_id) rather than a UUID.

    Does not support soft-delete (archive)—permission assignments are either active or deleted.

    Attributes:
        session: SQLAlchemy database session.
        model: The RolePermission model class.
        repository: SQLAlchemyRepository instance for database operations.
        entry_validator: Validates field-level data.
        entity_validator: Validates entity relationships and references.
        util: RBACUtils for RBAC helper functions.
        actor_id: UUID of the current user performing operations (for audit).
        domain: String identifier for this factory's domain ("RolePermission").

    Example:
        factory = RolePermissionFactory(session, current_user=admin_user)

        # Grant "edit_grades" permission to "teacher" role
        factory.create_role_permission(
            role_id=teacher_role.id,
            permission_id=edit_grades_permission.id
        )
    """

    def __init__(self, session: Session, model=RolePermission, current_user=None):
        """
        Initialize the RolePermissionFactory with database session and optional authenticated user.

        Args:
            session: SQLAlchemy database session for all operations.
            model: The model class to operate on. Defaults to RolePermission.
            current_user: The authenticated user performing operations. Used to
                populate audit fields (created_by, last_modified_by). Can be None
                for system-level operations.
        """
        super().__init__(current_user)
        self.session = session
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.entry_validator = EntryValidator()
        self.entity_validator = EntityValidator(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.util = RBACUtils()
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "RolePermission"

    def raise_not_found(self, identifier, error):
        """
        Raise a standardized EntityNotFoundError for role permission lookups.

        Args:
            identifier: The role permission ID or composite key that was not found.
            error: The original exception to include in the error message.

        Raises:
            EntityNotFoundError: Always raised with role permission-specific context.
        """
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name,
        )

    @resolve_fk_on_create()
    def create_role_permission(self, role_id, permission_id) -> RolePermission:
        """
        Assign a permission to a role.

        Creates a new role-permission association, granting the specified
        permission to users with the specified role.

        Args:
            role_id: UUID of the role to grant the permission to.
            permission_id: UUID of the permission to grant.

        Returns:
            RolePermission: The newly created assignment record.

        Raises:
            ForeignKeyViolationError: If role_id or permission_id reference
                non-existent entities (handled by @resolve_fk_on_create decorator).
            UniqueViolationError: If this permission is already assigned to
                this role (composite primary key constraint).

        Note:
            The combination of (role_id, permission_id) must be unique.
        """
        role_permission = RolePermission(
            role_id=role_id,
            permission_id=permission_id,
            created_by=self.actor_id,
            last_modified_by=self.actor_id,
        )

        return self.repository.create(role_permission)

    def get_role_permission(self, role_permission_id: UUID) -> RolePermission:
        """
        Retrieve a specific role-permission assignment by ID.

        Args:
            role_permission_id: The UUID or composite key of the assignment.

        Returns:
            RolePermission: The requested assignment record.

        Raises:
            EntityNotFoundError: If no assignment exists with the given ID.
        """
        try:
            return self.repository.get_by_id(role_permission_id)
        except EntityNotFoundError as e:
            self.raise_not_found(role_permission_id, e)

    def get_all_role_permissions(self, filters) -> List[RolePermission]:
        """
        Retrieve all role-permission assignments with optional filtering.

        Args:
            filters: Filter parameters for the query. Supports filtering by
                role_id and permission_id.

        Returns:
            List[RolePermission]: List of assignments matching the filters.

        Example:
            # Get all permissions for a specific role
            perms = factory.get_all_role_permissions({"role_id": teacher_role.id})

            # Get all roles that have a specific permission
            roles = factory.get_all_role_permissions({"permission_id": edit_perm.id})
        """
        fields = ["role_id", "permission_id"]
        return self.repository.execute_query(fields, filters)

    @resolve_fk_on_delete(display="RolePermission")
    def delete_role_permission(self, role_permission_id: UUID) -> None:
        """
        Revoke a permission from a role by deleting the assignment.

        This is a hard delete—the assignment cannot be recovered. To grant
        the permission again, create a new assignment.

        Args:
            role_permission_id: The UUID or composite key of the assignment to delete.

        Raises:
            EntityNotFoundError: If no assignment exists with the given ID.
            ForeignKeyViolationError: If other entities depend on this assignment
                (handled by @resolve_fk_on_delete decorator).
        """
        try:
            self.repository.delete(role_permission_id)

        except EntityNotFoundError as e:
            self.raise_not_found(role_permission_id, e)
