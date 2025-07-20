
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.core.academic_structure.models import Classes
from app.core.academic_structure.services.validators import AcademicStructureValidator
from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from app.core.shared.exceptions.maps.error_map import error_map


class ClassFactory(BaseFactory):
    """Factory class for managing class operations."""

    def __init__(self, session: Session, model=Classes, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session, model and current actor..
            Args:
                session: SQLAlchemy db session
                model: Model class, defaults to Classes
                current_user: The authenticated user performing the operation,
        """
        self.session = session
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = AcademicStructureValidator()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Class"


    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    @resolve_unique_violation({
        "classes_name_key": ("name", lambda self, data: data.name),
        "uq_class_level_order": ("order", lambda self, data: str(data.order)),
    })
    def create_class(self, data) -> Classes:
        """Create a new class.
        Args:
            data: class data containing name and description
        Returns:
            Classes: Created class record
        """

        from app.core.academic_structure.services.academic_structure import AcademicStructureService
        service = AcademicStructureService(self.session, self.current_user)

        new_class = Classes(
            id=uuid4(),
            level_id=data.level_id,
            order=service.create_class_order(data.level_id),
            code=data.code,

            created_by=self.actor_id,
            last_modified_by=self.actor_id,
        )
        return self.repository.create(new_class)


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
            self.raise_not_found(class_id, e)


    def get_all_classes(self, filters) -> List[Classes]:
        """Get all active classes with filtering.
        Returns:
            List[Classes]: List of active classes
        """
        fields = ['level_id', 'code']
        return self.repository.execute_query(fields, filters)


    @resolve_fk_on_update()
    @resolve_unique_violation({
        "classes_name_key": ("name", lambda self, *a: a[-1].get("name")),
        "uq_class_level_order": ("order", lambda self, *a: a[-1].get("order")),
    })
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

            for field, (validator_func, attr_name) in validations.items():
                if field in data:
                    setattr(existing, attr_name, validator_func(data.pop(field)))

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(class_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(class_id, e)


    def archive_class(self, class_id: UUID, reason) -> Classes:
        """Archive a class if there are no active dependencies.
        Args:
            class_id (UUID): ID of class to archive
            reason: Reason for archiving
        Returns:
        Classes: Archived class record
        """
        try:
            failed_dependencies = (
                self.archive_service.check_active_dependencies_exists(self.model, class_id)
                )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=class_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(class_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(class_id, e)


    @resolve_fk_on_delete()
    def delete_class(self, class_id: UUID, is_archived=False) -> None:
        """Permanently delete a class if there are no dependent entities
        Args:
            class_id (UUID): ID of class to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, class_id, is_archived)
            self.repository.delete(class_id)

        except EntityNotFoundError as e:
            self.raise_not_found(class_id, e)


    def get_all_archived_classes(self, filters) -> List[Classes]:
        """Get all archived classes with filtering.
        Returns:
            List[Classes]: List of archived class records
        """
        fields = ['level_id', 'code']
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
            self.raise_not_found(class_id, e)


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
            self.raise_not_found(class_id, e)


    @resolve_fk_on_delete()
    def delete_archived_class(self, class_id: UUID, is_archived=True) -> None:
        """Permanently delete an archived class if there are no dependent entities.
        Args:
            class_id: ID of class to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, class_id, is_archived)
            self.repository.delete_archive(class_id)

        except EntityNotFoundError as e:
            self.raise_not_found(class_id, e)
