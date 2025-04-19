from sqlalchemy.orm import Session
from uuid import uuid4, UUID

from ...errors.fk_resolver import FKResolver
from ...services.export_service.export import ExportService
from ...services.lifecycle_service.archive_service import ArchiveService
from ...services.lifecycle_service.delete_service import DeleteService
from ....core.validators.staff_organization import StaffOrganizationValidator
from ....database.models.staff_organization import StaffRole
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository

from ....core.errors.maps.error_map import error_map
from ....core.errors.maps.fk_mapper import fk_error_map
from ...errors import (
    DuplicateEntityError, ArchiveDependencyError, EntityNotFoundError, UniqueViolationError, RelationshipError
)


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class StaffRoleFactory:
    """Factory class for managing staff role operations."""

    def __init__(self, session: Session, model=StaffRole):
        """Initialize factory with database session.
        Args:
            session: SQLAlchemy database session
            model: Model class, defaults to StaffRole
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.export_service = ExportService(session)
        self.validator = StaffOrganizationValidator()
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.domain = "Staff role"


    def create_role(self, new_role) -> StaffRole:
        """Create a new staff role.
        Args:
            new_role: Role data containing name and description
        Returns:
            StaffRole: Created role record
        """
        role = StaffRole(
            id=uuid4(),
            name=self.validator.validate_name(new_role.name),
            description=self.validator.validate_description(new_role.description),
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
        )
        try:
            return self.repository.create(role)

        except UniqueViolationError as e:
            error_message = str(e).lower()
            unique_violation_map = {
                "staff_roles_name_key": ("phone", new_role.name)
            }
            for constraint_key, (field_name, entry_value) in unique_violation_map.items():
                if constraint_key in error_message:
                    raise DuplicateEntityError(
                        entity_model=self.entity_model, entry=entry_value, field=field_name,
                        display_name=self.display_name, detail=error_message
                    )
            raise DuplicateEntityError(
                entity_model=self.entity_model, entry="unknown", field='unknown',
                display_name="unknown", detail=error_message)

        except RelationshipError as e:
            resolved = FKResolver.resolve_fk_violation(
                factory_class=self.__class__, error_message=str(e), context_obj=new_role,
                operation="create", fk_map=fk_error_map
            )
            if resolved:
                raise resolved

            raise RelationshipError(
                error=str(e), operation="create", entity_model="unknown",domain=self.domain
            )


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
            raise EntityNotFoundError(
                entity_model = self.entity_model, identifier=role_id, error = str(e),
                display_name = self.display_name
            )


    def update_role(self, role_id: UUID, data: dict) -> StaffRole:
        """Update a staff role's information.
        Args:
            role_id: id of role to update
            data: Dictionary containing fields to update
        Returns:
            StaffRole: Updated role record
        """
        original = data.copy()
        try:
            existing = self.get_role(role_id)
            validations = {
                "name": (self.validator.validate_name, "name"),
                "description": (self.validator.validate_description, "description"),
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in data:
                    validated_value = validator_func(data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            existing.last_modified_by = SYSTEM_USER_ID
            return self.repository.update(role_id, existing)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=role_id, error=str(e),
                display_name=self.display_name
            )

        except UniqueViolationError as e:
            error_message = str(e).lower()
            unique_violation_map = {
                "staff_roles_name_key": ("phone", original.get('name', 'unknown'))
            }
            for constraint_key, (field_name, entry_value) in unique_violation_map.items():
                if constraint_key in error_message:
                    raise DuplicateEntityError(
                        entity_model=self.entity_model, entry=entry_value, field=field_name,
                        display_name=self.display_name, detail=error_message
                    )
            raise DuplicateEntityError(
                entity_model=self.entity_model, entry="unknown", field='unknown',
                display_name="unknown", detail=error_message)

        except RelationshipError as e:
            resolved = FKResolver.resolve_fk_violation(
                factory_class=self.__class__, error_message=str(e), context_obj=existing,
                operation="update", fk_map=fk_error_map
            )

            if resolved:
                raise resolved
            raise RelationshipError(
                error=str(e), operation="update", entity_model="unknown",domain=self.domain
            )


    def archive_role(self, role_id: UUID, reason) -> StaffRole:
        """Archive a role if no active staff members are assigned to it.
        Args:
            role_id: id of role to archive
            reason: Reason for archiving
        Returns:
            StaffRole: Archived role record
        """

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

            return self.repository.archive(role_id, SYSTEM_USER_ID, reason)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=role_id, error=str(e),
                display_name=self.display_name
            )


    def delete_role(self, role_id: UUID, is_archived = False) -> None:
        """Permanently delete a staff role if there are no dependent entities.
        Args:
            role_id: id of role to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, role_id, is_archived)
            return self.repository.delete(role_id)

        except EntityNotFoundError as e :
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=role_id, error=str(e),
                display_name=self.display_name
            )

        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model='unknown_entity', domain=self.domain)


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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=role_id, error=str(e),
                display_name=self.display_name
            )


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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=role_id, error=str(e),
                display_name=self.display_name
            )


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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=role_id, error=str(e),
                display_name=self.display_name
            )

        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model='unknown_entity', domain=self.domain)

