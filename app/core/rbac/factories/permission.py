
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.core.rbac.models import Permission
from app.core.rbac.services.permissions_service import PermissionService
from app.core.rbac.services.utils import RBACUtils
from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.validators.entity_validators import EntityValidator
from app.core.shared.validators.entry_validators import EntryValidator
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from app.core.shared.exceptions import EntityNotFoundError
from app.core.shared.exceptions.maps.error_map import error_map


class PermissionFactory(BaseFactory):
    """Factory class for managing permissions."""

    def __init__(self, session: Session, model=Permission, current_user=None):
        super().__init__(current_user)
        """Initialize factory with db session, model, and current actor.
            Args:
                session: SQLAlchemy db session
                model: Model class, defaults to Permission
                current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.entry_validator = EntryValidator()
        self.entity_validator = EntityValidator(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.service = PermissionService(self.session, current_user)
        self.util = RBACUtils()
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Permission"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    def create_permission(self, data) -> Permission:
        """Create a new permission."""

        permission = Permission(
            id=uuid4(),
            name=self.util.generate_permission_name(data.resource, data.action),
            resource = data.resource,
            action = data.action,
            description=self.entry_validator.validate_description(data.description, "RBAC permission"),
        )

        return self.repository.create(permission)


    def get_permission(self, permission_id: UUID) -> Permission:
        """Get a specific permission by ID."""
        try:
            return self.repository.get_by_id(permission_id)

        except EntityNotFoundError as e:
            self.raise_not_found(permission_id, e)


    @resolve_unique_violation({
        "permission_name_key": ("name", lambda self, _, data: data["name"])
    })
    @resolve_fk_on_update()
    def update_permission(self, permission_id: UUID, data: dict) -> Permission:
        """Update a permission information."""
        copied_data = data.copy()
        try:
            existing = self.get_permission(permission_id)

            if "description" in copied_data:
                self.entry_validator.validate_description(copied_data["description"], "RBAC permission")

            if "resource" in copied_data or "action" in copied_data:
                new_name = self.util.generate_permission_name(copied_data["resource"], copied_data["action"])
                setattr(existing, "name", new_name)

            for key, value in copied_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(permission_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(permission_id, e)


    def get_all_permissions(self, filters) -> List[Permission]:
        """Get all permissions"""
        fields = ['changed_by', 'staff_id']
        return self.repository.execute_query(fields, filters)


    def archive_permission(self, permission_id: UUID, reason) -> Permission:
        """Archive permission"""
        try:
            return self.repository.archive(permission_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(permission_id, e)


    @resolve_fk_on_delete(display="permission")
    def delete_permission(self, permission_id: UUID) -> None:
        """Permanently delete a permission if there are no dependent entities."""
        try:
            self.repository.delete(permission_id)

        except EntityNotFoundError as e:
            self.raise_not_found(permission_id, e)


    def get_all_archived_permissions(self, filters) -> List[Permission]:
        """Get all archived permissions with filtering"""
        fields = ['changed_by', 'staff_id']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_permission(self, permission_id: UUID) -> Permission:
        """Get an archived permission by ID."""
        try:
            return self.repository.get_archive_by_id(permission_id)
        except EntityNotFoundError as e:
            self.raise_not_found(permission_id, e)

    def restore_permission(self, permission_id: UUID) -> Permission:
        """Restore an archived permission."""
        try:
            return self.repository.restore(permission_id)
        except EntityNotFoundError as e:
            self.raise_not_found(permission_id, e)


    @resolve_fk_on_delete(display="permission")
    def delete_archived_permission(self, permission_id: UUID) -> None:
        """Permanently delete an archived permission if there are no dependent entities."""
        try:
            self.repository.delete_archive(permission_id)

        except EntityNotFoundError as e:
            self.raise_not_found(permission_id, e)
