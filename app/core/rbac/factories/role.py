from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.core.rbac.models import Role
from app.core.rbac.services.role_service import RBACService
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


class RoleFactory(BaseFactory):
    """
    Factory for managing Role entity lifecycle operations.

    Provides CRUD operations for roles with built-in validation, audit tracking,
    and soft-delete (archive) support. Handles foreign key and unique constraint
    violations through decorators that translate database errors into domain exceptions.

    Inherits from BaseFactory for common factory patterns including actor resolution
    for audit fields.

    Attributes:
        session: SQLAlchemy database session.
        model: The Role model class.
        repository: SQLAlchemyRepository instance for database operations.
        entry_validator: Validates field-level data (e.g., description format).
        entity_validator: Validates entity relationships and references.
        service: RBACService for role-specific business logic.
        util: RBACUtils for RBAC helper functions.
        actor_id: UUID of the current user performing operations (for audit).
        domain: String identifier for this factory's domain ("role").

    Example:
        factory = RoleFactory(session, current_user=admin_user)
        new_role = factory.create_role(CreateRoleSchema(name="TEACHER", ...))
    """

    def __init__(self, session: Session, model=Role, current_user=None):
        """Initialize factory with db session, model, and current actor.
            Args:
                session: SQLAlchemy db session
                model: Model class, defaults to Role
                current_user: The authenticated user performing the operation, if any.
        """
        super().__init__(current_user)

        self.session = session
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.entry_validator = EntryValidator()
        self.entity_validator = EntityValidator(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.service = RBACService(self.session)
        self.util = RBACUtils()
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "role"

    def raise_not_found(self, identifier, error):
        """
        Raise a standardized EntityNotFoundError for role lookups.
        Args:
            identifier: The role ID or identifier that was not found.
            error: The original exception to include in the error message.

        Raises:
            EntityNotFoundError: Always raised with role-specific context.
        """
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name,
        )

    @resolve_fk_on_create()
    def create_role(self, data) -> Role:
        """
        Create a new role in the system.

        Validates the description, generates a new UUID, and sets audit fields
        to the current actor.

        Args:
            data: Schema object containing:
                - name: UserRoleName enum value (must be unique).
                - description: Role description (validated for format).
                - rank: Optional integer for role hierarchy.
        Returns:
            Role: The newly created Role instance.

        Raises:
            ForeignKeyViolationError: If any referenced entities don't exist
                (handled by @resolve_fk_on_create decorator).

        Note:
            Unique constraint violations on name are handled at the database level.
        """

        role = Role(
            id=uuid4(),
            name=data.name,
            description=self.entry_validator.validate_description(
                data.description, "RBAC role"
            ),
            rank=data.rank,
            created_by=self.actor_id,
            last_modified_by=self.actor_id,
        )

        return self.repository.create(role)

    def get_role(self, role_id: UUID) -> Role:
        """Get a specific role by ID."""
        try:
            return self.repository.get_by_id(role_id)
        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)

    @resolve_unique_violation(
        {"role_name_key": ("name", lambda self, _, data: data["name"])}
    )
    @resolve_fk_on_update()
    def update_role(self, role_id: UUID, data: dict) -> Role:
        """
    Update an existing role's attributes.

    Supports partial updates—only provided fields are modified. Validates
    description and rank if included in the update data.

    Args:
        role_id: The UUID of the role to update.
        data: Dictionary of fields to update. Supported keys include:
            - name: New UserRoleName value.
            - description: New description (validated).
            - rank: New rank value (validated).

    Returns:
        Role: The updated Role instance.

    Raises:
        EntityNotFoundError: If no role exists with the given ID.
        UniqueViolationError: If updated name conflicts with existing role
            (handled by @resolve_unique_violation decorator).
        ForeignKeyViolationError: If any referenced entities don't exist
            (handled by @resolve_fk_on_update decorator).
    """
        copied_data = data.copy()

        try:
            existing = self.get_role(role_id)

            if "description" in copied_data:
                self.entry_validator.validate_description(
                    copied_data["description"], "RBAC role"
                )

            if "rank" in copied_data:
                self.util.validate_rank_number(copied_data["rank"])

            for key, value in copied_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(role_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)

    def get_all_roles(self, filters) -> List[Role]:
        """
        Retrieve all active (non-archived) roles with optional filtering.

        Args:
            filters: Filter parameters for the query. Supports filtering by
                fields like changed_by, staff_id, etc.

        Returns:
            List[Role]: List of Role instances matching the filters.
        """
        fields = ["changed_by", "staff_id"]
        return self.repository.execute_query(fields, filters)

    def archive_role(self, role_id: UUID, reason) -> Role:
        """
        Soft-delete a role by moving it to archived state.

        Archived roles are hidden from normal queries but can be restored.
        Preserves the role data and relationships for audit purposes.

        Args:
            role_id: The UUID of the role to archive.
            reason: Required explanation for why the role is being archived.

        Returns:
            Role: The archived Role instance.

        Raises:
            EntityNotFoundError: If no role exists with the given ID.
        """
        try:
            return self.repository.archive(role_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)

    @resolve_fk_on_delete(display="role")
    def delete_role(self, role_id: UUID) -> None:
        """
        Permanently delete a role from the database.

        This is a hard delete—the role cannot be recovered. Use archive_role() for soft-deletion.

        Args:
            role_id: The UUID of the role to delete.

        Raises:
            EntityNotFoundError: If no role exists with the given ID.
            ForeignKeyViolationError: If other entities reference this role
                (e.g., staff members assigned to it). Handled by
                @resolve_fk_on_delete decorator.
        """
        try:
            self.repository.delete(role_id)

        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)

    def get_all_archived_roles(self, filters) -> List[Role]:
        """
        Retrieve all archived roles with optional filtering.

        Args:
            filters: Filter parameters for the query.

        Returns:
            List[Role]: List of archived Role instances matching the filters.
        """

        fields = ["changed_by", "staff_id"]
        return self.repository.execute_archive_query(fields, filters)

    def get_archived_role(self, role_id: UUID) -> Role:
        """
        Retrieve a specific archived role by ID.

        Args:
            role_id: The UUID of the archived role to retrieve.

        Returns:
            Role: The archived Role instance.

        Raises:
            EntityNotFoundError: If no archived role exists with the given ID.
        """
        try:
            return self.repository.get_archive_by_id(role_id)
        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)

    def restore_role(self, role_id: UUID) -> Role:
        """
        Restore an archived role to active state.

        Args:
            role_id: The UUID of the archived role to restore.

        Returns:
            Role: The restored Role instance (now active).

        Raises:
            EntityNotFoundError: If no archived role exists with the given ID.
        """
        try:
            return self.repository.restore(role_id)
        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)

    @resolve_fk_on_delete(display="role")
    def delete_archived_role(self, role_id: UUID) -> None:
        """
        Permanently delete an archived role from the database.

        Args:
            role_id: The UUID of the archived role to delete.

        Raises:
            EntityNotFoundError: If no archived role exists with the given ID.
            ForeignKeyViolationError: If other entities still reference this role
                (handled by @resolve_fk_on_delete decorator).
        """
        try:
            self.repository.delete_archive(role_id)

        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)
