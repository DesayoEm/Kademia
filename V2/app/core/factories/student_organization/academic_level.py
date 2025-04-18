from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from ...errors.fk_resolver import FKResolver
from ...services.export_service.export import ExportService
from ...services.lifecycle_service.archive_service import ArchiveService
from ...services.lifecycle_service.delete_service import DeleteService
from ...validators.entity_validators import EntityValidator
from ....core.services.student_organization.academic_level import AcademicLevelService
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....database.models.enums import ArchiveReason
from ....core.validators.student_organization import StudentOrganizationValidator
from ....database.models.student_organization import AcademicLevel

from ....core.errors.maps.error_map import error_map
from ....core.errors.maps.fk_mapper import fk_error_map
from ...errors import (
    DuplicateEntityError, ArchiveDependencyError, EntityNotFoundError, UniqueViolationError, RelationshipError
)



SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class AcademicLevelFactory:
    """Factory class for managing academic level operations."""

    def __init__(self, session: Session, model = AcademicLevel):
        """Initialize factory with database session.
            Args:
            session: SQLAlchemy database session
            model: Model class, defaults to StudentDepartment
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.entity_validator = EntityValidator(session)
        self.validator = StudentOrganizationValidator()
        self.repository = SQLAlchemyRepository(self.model, session)
        self.service = AcademicLevelService
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.export_service = ExportService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.domain = "Academic level"


    def create_academic_level(self, new_academic_level) -> AcademicLevel:
        """Create a new academic level.
        Args:
            new_academic_level: Academic_level data containing name and description
        Returns:
            AcademicLevel: Created academic_level record
        """
        academic_level = AcademicLevel(
            id = uuid4(),
            name = self.validator.validate_level_name(new_academic_level.name),
            description = self.validator.validate_description(new_academic_level.description),
            order = self.service.return_default_order,

            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID
        )
        try:
            return self.repository.create(academic_level)

        except UniqueViolationError as e:
            error_message = str(e).lower()

            unique_violation_map = {
                "academic_levels_name_key": ("name", new_academic_level.name),
                "academic_levels_order_key": ("order", str(new_academic_level.order)),
            }

            for constraint_key, (field_name, entry_value) in unique_violation_map.items():
                if constraint_key in error_message:
                    raise DuplicateEntityError(
                        entity_model=self.entity_model, entry=entry_value, field=field_name,
                        display_name=self.display_name, detail=error_message
                    )

                raise DuplicateEntityError(
                    entity_model=self.entity_model, entry="unknown", field="unknown",
                    display_name=self.display_name, detail=error_message
                )

        except RelationshipError as e:
            resolved = FKResolver.resolve_fk_violation(
                factory_class=self.__class__, error_message=str(e), context_obj=new_academic_level,
                operation="create", fk_map=fk_error_map
            )
            if resolved:
                raise resolved
            raise RelationshipError(
                    error=str(e), operation="create", entity_model="unknown", domain=self.domain
                )


    def get_academic_level(self, academic_level_id: UUID) -> AcademicLevel:
        """Get a specific academic level by ID.
        Args:
            academic_level_id (UUID): ID of academic_level to retrieve
        Returns:
            AcademicLevel: Retrieved academic_level record
        """
        try:
            return self.repository.get_by_id(academic_level_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=academic_level_id, error=str(e),
                display_name=self.display_name
            )


    def get_all_academic_levels(self, filters) -> List[AcademicLevel]:
        """Get all active academic_levels with filtering.
        Returns:
            List[AcademicLevel]: List of active academic_levels
        """
        fields = ['name']
        return self.repository.execute_query(fields, filters)


    def update_academic_level(self, academic_level_id: UUID, data: dict) -> AcademicLevel:
        """Update an academic level's information.
        Args:
            academic_level_id (UUID): ID of academic_level to update
            data (dict): Dictionary containing fields to update
        Returns:
            AcademicLevel: Updated academic_level record
        """
        original = data.copy()
        try:
            existing = self.get_academic_level(academic_level_id)
            validations = {
                "name": (self.validator.validate_level_name, "name"),
                "description": (self.validator.validate_description, "description"),
                "order": (self.validator.validate_order, "order"),
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in data:
                    validated_value = validator_func(data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            existing.last_modified_by = SYSTEM_USER_ID

            return self.repository.update(academic_level_id, existing)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=academic_level_id, error=str(e),
                display_name=self.display_name
            )

        except UniqueViolationError as e:
            error_message = str(e).lower()
            unique_violation_map = {
                "academic_levels_name_key": ("name", data.get('name', 'unknown')),
                "academic_levels_order_key": ("order", str(data.get('order', 'unknown'))),
            }

            for constraint_key, (field_name, entry_value) in unique_violation_map.items():
                if constraint_key in error_message:
                    raise DuplicateEntityError(
                        entity_model=self.entity_model, entry=entry_value, field=field_name,
                        display_name=self.display_name, detail=error_message
                    )

                raise DuplicateEntityError(
                    entity_model=self.entity_model, entry="unknown", field="unknown",
                    display_name=self.display_name, detail=error_message
                )

        except RelationshipError as e:
            resolved = FKResolver.resolve_fk_violation(
                factory_class=self.__class__, error_message=str(e), context_obj=existing,
                operation="update", fk_map=fk_error_map
            )
            if resolved:
                raise resolved

            raise RelationshipError(
                error=str(e), operation="update", entity_model="unknown", domain=self.domain
            )


    def archive_academic_level(self, academic_level_id: UUID, reason: ArchiveReason) -> AcademicLevel:
        """Archive aN academic level.
        Args:
            academic_level_id (UUID): ID of academic_level to archive
            reason (ArchiveReason): Reason for archiving
        Returns:
            AcademicLevel: Archived academic_level record
        """
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=academic_level_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=academic_level_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(academic_level_id, SYSTEM_USER_ID, reason)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=academic_level_id, error=str(e),
                display_name=self.display_name
            )


    def delete_academic_level(self, academic_level_id: UUID, is_archived=False) -> None:
        """Permanently delete an academic level if there are no dependent entities
        Args:
            academic_level_id (UUID): ID of academic_level to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, academic_level_id, is_archived)
            return self.repository.delete(academic_level_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=academic_level_id, error=str(e),
                display_name=self.display_name
            )

        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model=self.model.__name__, domain = self.domain)


    def get_all_archived_academic_levels(self, filters) -> List[AcademicLevel]:
        """Get all archived academic_levels with filtering.
        Returns:
            List[AcademicLevel]: List of archived academic_level records
        """
        fields = ['name']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_academic_level(self, academic_level_id: UUID) -> AcademicLevel:
        """Get an archived academic_level by ID.
        Args:
            academic_level_id: ID of academic_level to retrieve
        Returns:
            AcademicLevel: Retrieved academic_level record
        """
        try:
            return self.repository.get_archive_by_id(academic_level_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=academic_level_id, error=str(e),
                display_name=self.display_name
            )


    def restore_academic_level(self, academic_level_id: UUID) -> AcademicLevel:
        """Restore an archived academic_level.
        Args:
            academic_level_id: ID of academic_level to restore
        Returns:
            AcademicLevel: Restored academic_level record
        """
        try:
            return self.repository.restore(academic_level_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=academic_level_id, error=str(e),
                display_name=self.display_name
            )


    def delete_archived_academic_level(self, academic_level_id: UUID, is_archived = True) -> None:
        """Permanently delete an archived academic_level if there are no dependent entities.
        Args:
            academic_level_id: ID of academic_level to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, academic_level_id, is_archived)
            self.repository.delete_archive(academic_level_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=academic_level_id, error=str(e),
                display_name=self.display_name
            )

        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model='unknown_entity', domain=self.domain)

