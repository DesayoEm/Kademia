from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from ....core.services.student_organization.classes import ClassService
from V2.app.database.models.student_organization import Classes
from ....core.validators.student_organization import StudentOrganizationValidator
from V2.app.core.shared.services.export_service import ExportService
from V2.app.core.shared.services.lifecycle_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service import DeleteService
from V2.app.core.shared.validators.entity_validators import EntityValidator
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository

from V2.app.core.shared.errors.fk_resolver import FKResolver
from ....core.errors.maps.error_map import error_map
from ....core.errors.maps.fk_mapper import fk_error_map
from V2.app.core.shared.errors import (
    DuplicateEntityError, ArchiveDependencyError, EntityNotFoundError, UniqueViolationError, RelationshipError
)


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class ClassFactory:
    """Factory class for managing class operations."""

    def __init__(self, session: Session, model = Classes):
        """Initialize factory with model and database session.
            Args:
                session: SQLAlchemy database session
                model: Model class, defaults to Classes
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.entity_validator = EntityValidator(session)
        self.validator = StudentOrganizationValidator()
        self.repository = SQLAlchemyRepository(self.model, session)
        self.service = ClassService(session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.export_service = ExportService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.domain = "Class"


    def create_class(self, new_class) -> Classes:
        """Create a new class.
        Args:
            new_class: class data containing name and description
        Returns:
            Classes: Created class record
        """
        class_data = Classes(
            id = uuid4(),
            level_id = new_class.level_id,
            order = self.service.create_order(new_class.level_id),
            code=new_class.code,

            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,

        )
        try:
            return self.repository.create(class_data)

        except UniqueViolationError as e:
            error_message = str(e).lower()
            unique_violation_map = {
                "uq_class_level_code": ("code", new_class.code.value),
                "uq_class_level_order": ("order", str(new_class.order)),
            }
            for constraint_key, (field_name, entry_value) in unique_violation_map.items():
                if constraint_key in error_message:
                    raise DuplicateEntityError(
                        entity_model=self.entity_model, entry=entry_value,
                        field=field_name, display_name=self.display_name,
                        detail=error_message
                    )

            raise DuplicateEntityError(
                entity_model=self.entity_model, entry="unknown",field="unknown",
                display_name=self.display_name, detail=error_message
            )

        except RelationshipError as e:
            resolved = FKResolver.resolve_fk_violation(
                factory_class=self.__class__, error_message=str(e), context_obj=new_class,
                operation="create", fk_map=fk_error_map
            )
            if resolved:
                raise resolved
            raise RelationshipError(
                error=str(e), operation="create", entity_model="unknown", domain=self.domain
            )


    def get_class(self, class_id: UUID) -> Classes:
        """Get a specific class by ID.
        Args:
            class_id (UUID): ID of class to retrieve
        Returns:
            Classes: Retrieved class record
        """
        try:
            return self.repository.get_by_id(class_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=class_id, error=str(e),
                display_name=self.display_name

            )


    def get_all_classes(self, filters) -> List[Classes]:
        """Get all active student_organization with filtering.
        Returns:
            List[Classes]: List of active student_organization
        """
        fields = ['level_id', 'code']
        return self.repository.execute_query(fields, filters)


    def update_class(self, class_id: UUID, data: dict) -> Classes:
        """Update a class's information.
        Args:
            class_id (UUID): ID of class to update
            data (dict): Dictionary containing fields to update
        Returns:
            Classes: Updated class record
        """
        original = data.copy()
        try:
            existing = self.get_class(class_id)

            validations = {
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
            return self.repository.update(class_id, existing)


        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=class_id, error=str(e),
                display_name=self.display_name
            )
        except UniqueViolationError as e:
            error_message = str(e).lower()
            unique_violation_map = {
                "uq_class_level_order": ("order", str(original.get('order', 'unknown')))
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


    def archive_class(self, class_id: UUID, reason) -> Classes:
        """Archive a class.
        Args:
            class_id (UUID): ID of class to archive
            reason: Reason for archiving
        Returns:
            Classes: Archived class record
        """
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=class_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=class_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(class_id, SYSTEM_USER_ID, reason)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=class_id, error=str(e),
                display_name=self.display_name
            )


    def delete_class(self, class_id: UUID, is_archived=False) -> None:
        """Permanently delete a class if there are no dependent entities
        Args:
            class_id (UUID): ID of class to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, class_id, is_archived)
            return self.repository.delete(class_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=class_id, error=str(e),
                display_name=self.display_name
            )

        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model=self.model.__name__, domain=self.domain)


    def get_all_archived_classes(self, filters) -> List[Classes]:
        """Get all archived student_organization with filtering.
        Returns:
            List[Classes]: List of archived class records
        """
        fields = ['code']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_class(self, class_id: UUID) -> Classes:
        """Get an archived class by ID.
        Args:
            class_id: ID of class to retrieve
        Returns:
            Classes: Retrieved class record
        """
        try:
            return self.repository.get_archive_by_id(class_id)
        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=class_id, error=str(e),
                display_name=self.display_name
            )

    def restore_class(self, class_id: UUID) -> Classes:
        """Restore an archived class.
        Args:
            class_id: ID of class to restore
        Returns:
            Classes: Restored class record
        """
        try:
            return self.repository.restore(class_id)
        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=class_id, error=str(e),
                display_name=self.display_name
            )


    def delete_archived_class(self, class_id: UUID, is_archived = True) -> None:
            """Permanently delete an archived class if there are no dependent entities.
            Args:
                class_id: ID of class to delete
                is_archived: Whether to check archived or active entities
            """
            try:
                self.delete_service.check_safe_delete(self.model, class_id, is_archived)
                self.repository.delete_archive(class_id)

            except EntityNotFoundError as e:
                raise EntityNotFoundError(
                    entity_model=self.entity_model, identifier=class_id, error=str(e),
                    display_name=self.display_name
                )

            except RelationshipError as e:  # Failsafe
                raise RelationshipError(
                    error=str(e), operation='delete', entity_model='unknown_entity', domain=self.domain)




