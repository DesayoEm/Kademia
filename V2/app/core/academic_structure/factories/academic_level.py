from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from V2.app.core.academic_structure.models.academic_structure import AcademicLevel
from V2.app.core.academic_structure.services.academic_level import AcademicLevelService
from V2.app.core.academic_structure.validators.academic_structure import AcademicStructureValidator
from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from V2.app.core.shared.exceptions.maps.error_map import error_map




class AcademicLevelFactory(BaseFactory):
    """Factory class for managing academic level operations."""

    def __init__(self, session: Session, model = AcademicLevel, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session, model and current actor.
            Args:
            session: SQLAlchemy db session
            model: Model class, defaults to AcademicLevel
            current_user: The authenticated user performing the operation, if any.
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.service = AcademicLevelService(session)
        self.validator = AcademicStructureValidator()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Academic Level"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )


    @resolve_unique_violation({
        "academic_levels_name_key": ("name", lambda self, data: data.name),
        "academic_levels_order_key": ("order", lambda self, data: data.order),
    })
    @resolve_fk_on_create()
    def create_academic_level(self, data) -> AcademicLevel:
        """Create a new academic level.
        Args:
            data: Academic_level data containing name and description
        Returns:
            AcademicLevel: Created academic_level record
        """
        new_level = AcademicLevel(
            id=uuid4(),
            name=self.validator.validate_level_name(data.name),
            description=self.validator.validate_description(data.description),
            order=self.service.return_default_order(),

            created_by=self.actor_id,
            last_modified_by=self.actor_id
        )
        return self.repository.create(new_level)


    def get_academic_level(self, level_id: UUID) -> AcademicLevel:
        """Get a specific academic level by ID.
        Args:
            level_id (UUID): ID of academic_level to retrieve
        Returns:
            AcademicLevel: Retrieved academic_level record
        """
        try:
            return self.repository.get_by_id(level_id)
        except EntityNotFoundError as e:
            self.raise_not_found(level_id, e)


    def get_all_academic_levels(self, filters) -> List[AcademicLevel]:
        """Get all active academic_levels with filtering.
        Returns:
            List[AcademicLevel]: List of active academic_levels
        """
        fields = ['name']
        return self.repository.execute_query(fields, filters)


    @resolve_unique_violation({
        "academic_levels_name_key": ("name", lambda self, *a: a[-1].get("name")),
        "academic_levels_order_key": ("order", lambda self, *a: a[-1].get("order")),
    })
    @resolve_fk_on_update()
    def update_academic_level(self, level_id: UUID, data: dict) -> AcademicLevel:
        """Update an academic level's information.
        Args:
            level_id (UUID): ID of academic_level to update
            data (dict): Dictionary containing fields to update
        Returns:
            AcademicLevel: Updated academic_level record
        """
        copied_data = data.copy()
        try:
            existing = self.get_academic_level(level_id)
            validations = {
                "name": (self.validator.validate_level_name, "name"),
                "description": (self.validator.validate_description, "description"),
                "order": (self.validator.validate_order, "order"),
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in copied_data:
                    validated_value = validator_func(copied_data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in copied_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(level_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
                self.raise_not_found(level_id, e)


    def archive_academic_level(self, level_id: UUID, reason) -> AcademicLevel:
        """Archive an academic level no active dependencies exist.
        Args:
            level_id (UUID): ID of academic_level to archive
            reason: Reason for archiving
        Returns:
            AcademicLevel: Archived academic_level record
        """
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=level_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=level_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(level_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(level_id, e)


    @resolve_fk_on_delete()
    def delete_academic_level(self, level_id: UUID, is_archived=False) -> None:
        """Permanently delete an academic level if there are no dependent entities
        Args:
            level_id (UUID): ID of academic_level to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, level_id, is_archived)
            return self.repository.delete(level_id)

        except EntityNotFoundError as e:
            self.raise_not_found(level_id, e)

    def get_all_archived_academic_levels(self, filters) -> List[AcademicLevel]:
        """Get all archived academic_levels with filtering.
        Returns:
            List[AcademicLevel]: List of archived academic_level records
        """
        fields = ['name']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_academic_level(self, level_id: UUID) -> AcademicLevel:
        """Get an archived academic_level by ID.
        Args:
            level_id: ID of academic_level to retrieve
        Returns:
            AcademicLevel: Retrieved academic_level record
        """
        try:
            return self.repository.get_archive_by_id(level_id)
        except EntityNotFoundError as e:
            self.raise_not_found(level_id, e)


    def restore_academic_level(self, level_id: UUID) -> AcademicLevel:
        """Restore an archived academic_level.
        Args:
            level_id: ID of academic_level to restore
        Returns:
            AcademicLevel: Restored academic_level record
        """
        try:
            return self.repository.restore(level_id)
        except EntityNotFoundError as e:
            self.raise_not_found(level_id, e)


    @resolve_fk_on_delete()
    def delete_archived_academic_level(self, level_id: UUID, is_archived = True) -> None:
        """Permanently delete an archived academic_level if there are no dependent entities.
        Args:
            level_id: ID of academic_level to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, level_id, is_archived)
            self.repository.delete_archive(level_id)

        except EntityNotFoundError as e:
            self.raise_not_found(level_id, e)
