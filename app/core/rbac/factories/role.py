
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.core.rbac.models import Role
from app.core.rbac.services.role_service import RoleChangeService
from app.core.rbac.services.utils import RBACUtils
from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.validators.entity_validators import EntityValidator
from app.core.shared.validators.entry_validators import EntryValidator
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from app.core.shared.exceptions import EntityNotFoundError
from app.core.shared.exceptions.maps.error_map import error_map


class RoleFactory(BaseFactory):
    """Factory class for managing roles."""

    def __init__(self, session: Session, model=Role, current_user=None):
        super().__init__(current_user)
        """Initialize factory with db session, model, and current actor.
            Args:
                session: SQLAlchemy db session
                model: Model class, defaults to Role
                current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.entry_validator = EntryValidator()
        self.entity_validator = EntityValidator(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.service = RoleChangeService()
        self.util = RBACUtils()
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "role"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    def create_role(self, data) -> Role:
        """Create a new role."""

        role = Role(
            id=uuid4(),
            name=data.name,
            description=self.entry_validator.validate_description(data.description, "RBAC role"),
            rank= data.rank,

            created_by = self.actor_id,
            last_modified_by = self.actor_id
        )

        return self.repository.create(role)


    def get_role(self, role_id: UUID) -> Role:
        """Get a specific role by ID."""
        try:
            return self.repository.get_by_id(role_id)
        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)

    @resolve_unique_violation({
        "role_name_key": ("name", lambda self, _, data: data["name"])
    })
    @resolve_fk_on_update()
    def update_role(self, role_id: UUID, data: dict) -> Role:
        """Update a role information."""
        copied_data = data.copy()
        try:
            existing = self.get_role(role_id)

            if "description" in copied_data:
                self.entry_validator.validate_description(copied_data["description"], "RBAC role")

            if "rank" in copied_data:
                self.util.validate_rank_number(copied_data["rank"])

            for key, value in copied_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(role_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)


    def get_all_roles(self, filters) -> List[Role]:
        """Get all roles"""
        fields = ['changed_by', 'staff_id']
        return self.repository.execute_query(fields, filters)


    def archive_role(self, role_id: UUID, reason) -> Role:
        """Archive role"""
        try:
            return self.repository.archive(role_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)


    @resolve_fk_on_delete(display="role")
    def delete_role(self, role_id: UUID) -> None:
        """Permanently delete a role if there are no dependent entities."""
        try:
            self.repository.delete(role_id)

        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)


    def get_all_archived_roles(self, filters) -> List[Role]:
        """Get all archived roles with filtering"""
        fields = ['changed_by', 'staff_id']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_role(self, role_id: UUID) -> Role:
        """Get an archived role by ID."""
        try:
            return self.repository.get_archive_by_id(role_id)
        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)


    def restore_role(self, role_id: UUID) -> Role:
        """Restore an archived role."""
        try:
            return self.repository.restore(role_id)
        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)


    @resolve_fk_on_delete(display="role")
    def delete_archived_role(self, role_id: UUID) -> None:
        """Permanently delete an archived role if there are no dependent entities."""
        try:
            self.repository.delete_archive(role_id)

        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)
