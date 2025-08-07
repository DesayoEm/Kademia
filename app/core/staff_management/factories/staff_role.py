from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.services.audit_export_service.export import ExportService
from app.core.staff_management.services.validators import StaffManagementValidator
from app.core.staff_management.models import StaffRole
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from app.core.shared.exceptions.maps.error_map import error_map



class StaffRoleFactory(BaseFactory):
    """Factory class for managing staff role operations."""

    def __init__(self, session: Session, model=StaffRole, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session.
        Args:
            session: SQLAlchemy db session
            model: Model class, defaults to StaffRole
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session, current_user)
        self.export_service = ExportService(session)
        self.validator = StaffManagementValidator()
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Staff Role"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    @resolve_unique_violation({
        "staff_roles_name_key": ("name", lambda self, data: data.name),
    })
    def create_role(self, data) -> StaffRole:
        """Create a new staff role.
        Args:
            data: Role data containing name and description
        Returns:
            StaffRole: Created role record
        """
        role = StaffRole(
            id=uuid4(),
            name=self.validator.validate_name(data.name),
            description=self.validator.validate_description(data.description),
            created_by=self.actor_id,
            last_modified_by=self.actor_id,
        )

        return self.repository.create(role)


    def get_all_roles(self, filters) -> list[StaffRole]:
        """Get all active staff roles with filtering.
        Returns:
            List[StaffRole]: List of active role records
        """
        fields = ['name']
        return self.repository.execute_query(fields, filters)


    def get_role(self, role_id: UUID) -> StaffRole:
        """Get a specific staff role by id.
        Args:
            role_id: id of role to retrieve
        Returns:
            StaffRole: Retrieved role record
        """
        try:
            return self.repository.get_by_id(role_id)
        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)

    @resolve_fk_on_update()
    @resolve_unique_violation({
        "staff_roles_name_key": ("name", lambda self, *a: a[-1].get("name")),
    })
    def update_role(self, role_id: UUID, data: dict) -> StaffRole:
        """Update a staff role's information.
        Args:
            role_id: id of role to update
            data: Dictionary containing fields to update
        Returns:
            StaffRole: Updated role record
        """
        copied_data = data.copy()
        try:
            existing = self.get_role(role_id)
            validations = {
                "name": (self.validator.validate_name, "name"),
                "description": (self.validator.validate_description, "description"),
            }

            # leave original data untouched for error message extraction
            for field, (validator_func, model_attr) in validations.items():
                if field in copied_data:
                    validated_value = validator_func(copied_data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in copied_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(role_id, existing,modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)


    def archive_role(self, role_id: UUID, reason) -> StaffRole:
        """Archive a role if no active staff members are assigned to it."""
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=role_id
            )

            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=role_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(role_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)


    @resolve_fk_on_delete()
    def delete_role(self, role_id: UUID, is_archived = False) -> None:
        """Permanently delete a staff role if there are no dependent entities.
        Args:
            role_id: id of role to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, role_id, is_archived)
            return self.repository.delete(role_id)

        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)


    #Archive methods
    def get_all_archived_roles(self, filters) -> list[StaffRole]:
        """Get all archived staff roles with filtering.
        Returns:
            List[StaffRole]: List of archived role records
        """
        fields = ['name']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_role(self, role_id: UUID) -> StaffRole:
        """Get an archived role by ID.
        Args:
            role_id: id of role to retrieve
        Returns:
            StaffRole: Retrieved role record
        """
        try:
            return self.repository.get_archive_by_id(role_id)
        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)


    def restore_role(self, role_id: UUID) -> StaffRole:
        """Restore an archived role.
        Args:
            role_id: id of role to restore
        Returns:
            StaffRole: Restored role record
        """
        try:
            return self.repository.restore(role_id)
        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)


    @resolve_fk_on_delete()
    def delete_archived_role(self, role_id: UUID, is_archived = True) -> None:
        """Permanently delete an archived role if there are no dependent entities.
        Args:
            role_id: id of role to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, role_id, is_archived)
            self.repository.delete_archive(role_id)

        except EntityNotFoundError as e:
            self.raise_not_found(role_id, e)