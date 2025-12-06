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
    """Factory class for managing RolePermissions."""

    def __init__(self, session: Session, model=RolePermission, current_user=None):
        super().__init__(current_user)
        """Initialize factory with db session, model, and current actor.
            Args:
                session: SQLAlchemy db session
                model: Model class, defaults to RolePermission
                current_user: The authenticated user performing the operation, if any.
        """
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
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name,
        )

    @resolve_fk_on_create()
    def create_role_permission(self, role_id, permission_id) -> RolePermission:
        """Create a new role permission."""
        role_permission = RolePermission(
            role_id=role_id,
            permission_id=permission_id,
            created_by=self.actor_id,
            last_modified_by=self.actor_id,
        )

        return self.repository.create(role_permission)

    def get_role_permission(self, role_permission_id: UUID) -> RolePermission:
        """Get a specific role permission by ID."""
        try:
            return self.repository.get_by_id(role_permission_id)
        except EntityNotFoundError as e:
            self.raise_not_found(role_permission_id, e)

    def get_all_role_permissions(self, filters) -> List[RolePermission]:
        """Get all role permissions"""
        fields = ["role_id", "permission_id"]
        return self.repository.execute_query(fields, filters)

    @resolve_fk_on_delete(display="RolePermission")
    def delete_role_permission(self, role_permission_id: UUID) -> None:
        """Permanently delete a role permission"""
        try:
            self.repository.delete(role_permission_id)

        except EntityNotFoundError as e:
            self.raise_not_found(role_permission_id, e)

    # def get_all_archived_role_permissions(self, filters) -> List[RolePermission]:
    #     """Get all archived RolePermissions with filtering"""
    #     fields = ['changed_by', 'staff_id']
    #     return self.repository.execute_archive_query(fields, filters)
    #
    #
    # def get_archived_role_permission(self, role_permission_id: UUID) -> RolePermission:
    #     """Get an archived RolePermission by ID."""
    #     try:
    #         return self.repository.get_archive_by_id(role_permission_id)
    #     except EntityNotFoundError as e:
    #         self.raise_not_found(role_permission_id, e)
    #
    #
    # def restore_role_permission(self, role_permission_id: UUID) -> RolePermission:
    #     """Restore an archived RolePermission."""
    #     try:
    #         return self.repository.restore(role_permission_id)
    #     except EntityNotFoundError as e:
    #         self.raise_not_found(role_permission_id, e)
    #
    #
    # @resolve_fk_on_delete(display="RolePermission")
    # def delete_archived_role_permission(self, role_permission_id: UUID) -> None:
    #     """Permanently delete an archived RolePermission if there are no dependent entities."""
    #     try:
    #         self.repository.delete_archive(role_permission_id)
    #
    #     except EntityNotFoundError as e:
    #         self.raise_not_found(role_permission_id, e)
