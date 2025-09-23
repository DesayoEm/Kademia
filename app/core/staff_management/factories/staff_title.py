from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from app.core.shared.factory.base_factory import BaseFactory
from app.core.staff_management.services.validators import StaffManagementValidator
from app.core.staff_management.models import StaffJobTitle
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError, DeletionDependencyError
from app.core.shared.exceptions.maps.error_map import error_map



class StaffTitleFactory(BaseFactory):
    """Factory class for managing staff title operations."""

    def __init__(self, session: Session, model=StaffJobTitle, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session.
        Args:
            session: SQLAlchemy db session
            model: Model class, defaults to StaffTitle
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session, current_user)
        self.validator = StaffManagementValidator()
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Staff Title"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    @resolve_unique_violation({
        "staff_titles_name_key": ("name", lambda self, data: data.name),
    })
    def create_title(self, data) -> StaffJobTitle:
        """Create a new staff title.
        Args:
            data: title data containing name and description
        Returns:
            StaffJobTitle: Created title record
        """
        title = StaffJobTitle(
            id=uuid4(),
            name=self.validator.validate_name(data.name),
            description=self.validator.validate_description(data.description),
            created_by=self.actor_id,
            last_modified_by=self.actor_id,
        )

        return self.repository.create(title)


    def get_all_titles(self, filters) -> list[StaffJobTitle]:
        """Get all active staff titles with filtering.

        Returns:
            List[StaffJobTitle]: List of active title records
        """
        fields = ['name']
        return self.repository.execute_query(fields, filters)


    def get_title(self, title_id: UUID) -> StaffJobTitle:
        """Get a specific staff title by id.
        Args:
            title_id: id of title to retrieve
        Returns:
            StaffJobTitle: Retrieved title record
        """
        try:
            return self.repository.get_by_id(title_id)
        except EntityNotFoundError as e:
            self.raise_not_found(title_id, e)


    @resolve_fk_on_update()
    @resolve_unique_violation({
        "staff_titles_name_key": ("name", lambda self, *a: a[-1].get("name")),
    })
    def update_title(self, title_id: UUID, data: dict) -> StaffJobTitle:
        """Update a staff title's information.
        Args:
            title_id: id of title to update
            data: Dictionary containing fields to update
        Returns:
            StaffJobTitle: Updated title record
        """
        copied_data = data.copy()
        try:
            existing = self.get_title(title_id)
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

            return self.repository.update(title_id, existing,modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(title_id, e)


    def archive_title(self, title_id: UUID, reason) -> StaffJobTitle:
        """Archive a title if no active staff members are assigned to it."""
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=title_id
            )

            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=title_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(title_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(title_id, e)


    @resolve_fk_on_delete(display="title")
    def delete_title(self, title_id: UUID) -> None:
        """Permanently delete a staff title if there are no dependent entities.
        Args:
            title_id: id of title to delete
        """
        try:
            failed_dependencies = self.delete_service.check_active_dependencies_exists(self.model, title_id)

            if failed_dependencies:
                raise DeletionDependencyError(
                    entity_model=self.entity_model, identifier=title_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )

            return self.repository.delete(title_id)

        except EntityNotFoundError as e:
            self.raise_not_found(title_id, e)


    #Archive methods
    def get_all_archived_titles(self, filters) -> list[StaffJobTitle]:
        """Get all archived staff titles with filtering.
        Returns:
            List[StaffJobTitle]: List of archived title records
        """
        fields = ['name']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_title(self, title_id: UUID) -> StaffJobTitle:
        """Get an archived title by ID.
        Args:
            title_id: id of title to retrieve
        Returns:
            StaffJobTitle: Retrieved title record
        """
        try:
            return self.repository.get_archive_by_id(title_id)
        except EntityNotFoundError as e:
            self.raise_not_found(title_id, e)


    def restore_title(self, title_id: UUID) -> StaffJobTitle:
        """Restore an archived title.
        Args:
            title_id: id of title to restore
        Returns:
            StaffJobTitle: Restored title record
        """
        try:
            return self.repository.restore(title_id)
        except EntityNotFoundError as e:
            self.raise_not_found(title_id, e)


    @resolve_fk_on_delete(display="title")
    def delete_archived_title(self, title_id: UUID) -> None:
        """Permanently delete an archived title if there are no dependent entities.
        Args:
            title_id: id of title to delete
        """
        try:
            failed_dependencies = self.delete_service.check_active_dependencies_exists(self.model, title_id)

            if failed_dependencies:
                raise DeletionDependencyError(
                    entity_model=self.entity_model, identifier=title_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            self.repository.delete_archive(title_id)

        except EntityNotFoundError as e:
            self.raise_not_found(title_id, e)