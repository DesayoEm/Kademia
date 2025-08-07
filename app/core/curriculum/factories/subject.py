from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.core.curriculum.models.curriculum import Subject
from app.core.curriculum.services.validators import CurriculumValidator
from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from app.core.shared.exceptions.maps.error_map import error_map


class SubjectFactory(BaseFactory):
    """Factory class for managing subject operations."""

    def __init__(self, session: Session, model = Subject, current_user = None):
        super().__init__(current_user)
        """Initialize factory.
            Args:
            session: SQLAlchemy db session
            model: Model class, defaults to Subject
            current_user: The authenticated user performing the operation, if any.
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = CurriculumValidator()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session,current_user)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Subject"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_unique_violation({
        "subjects_name_key": ("name", lambda self, _, data: data.name)
    })
    @resolve_fk_on_create()
    def create_subject(self, data) -> Subject:
        """Create a new subject.
        Args:
            data: Subject data
        Returns:
            Subject: Created subject recorda
        """
        new_subject = Subject(
            id=uuid4(),
            name=self.validator.validate_name(data.name),
            department_id=data.department_id,

            created_by=self.actor_id,
            last_modified_by=self.actor_id
        )
        return self.repository.create(new_subject)


    def get_subject(self, subject_id: UUID) -> Subject:
        """Get a specific subject by ID.
        Args:
            subject_id (UUID): ID of subject to retrieve
        Returns:
            Subject: Retrieved subject record
        """
        try:
            return self.repository.get_by_id(subject_id)
        except EntityNotFoundError as e:
            self.raise_not_found(subject_id, e)


    def get_all_subjects(self, filters) -> List[Subject]:
        """Get all active subjects with filtering.
        Returns:
            List[Subject]: List of active subjects
        """
        fields = ['name', 'department_id']
        return self.repository.execute_query(fields, filters)


    @resolve_unique_violation({
        "subjects_name_key": ("name", lambda self, _, data: data["name"])
    })
    @resolve_fk_on_update()
    def update_subject(self, subject_id: UUID, data: dict) -> Subject:
        """Update a subject's information.
        Args:
            subject_id (UUID): ID of subject to update
            data (dict): Dictionary containing fields to update
        Returns:
            Subject: Updated subject record
        """
        copied_data = data.copy()
        try:
            existing = self.get_subject(subject_id)
            validations = {
                "name": (self.validator.validate_name, "name"),
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in copied_data:
                    validated_value = validator_func(copied_data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in copied_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(subject_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
                self.raise_not_found(subject_id, e)


    def archive_subject(self, subject_id: UUID, reason) -> Subject:
        """Archive a subject if no active dependencies exist.
        Args:
            subject_id (UUID): ID of subject to archive
            reason: Reason for archiving
        Returns:
            Subject: Archived subject record
        """
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=subject_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=subject_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(subject_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(subject_id, e)


    @resolve_fk_on_delete()
    def delete_subject(self, subject_id: UUID, is_archived=False) -> None:
        """Permanently delete a subject if there are no dependent entities
        Args:
            subject_id (UUID): ID of subject to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, subject_id, is_archived)
            return self.repository.delete(subject_id)

        except EntityNotFoundError as e:
            self.raise_not_found(subject_id, e)

    def get_all_archived_subjects(self, filters) -> List[Subject]:
        """Get all archived subjects with filtering.
        Returns:
            List[Subject]: List of archived subject records
        """
        fields = ['name', 'department_id']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_subject(self, subject_id: UUID) -> Subject:
        """Get an archived subject by ID.
        Args:
            subject_id: ID of subject to retrieve
        Returns:
            Subject: Retrieved subject record
        """
        try:
            return self.repository.get_archive_by_id(subject_id)
        except EntityNotFoundError as e:
            self.raise_not_found(subject_id, e)


    def restore_subject(self, subject_id: UUID) -> Subject:
        """Restore an archived subject.
        Args:
            subject_id: ID of subject to restore
        Returns:
            Subject: Restored subject record
        """
        try:
            return self.repository.restore(subject_id)
        except EntityNotFoundError as e:
            self.raise_not_found(subject_id, e)


    @resolve_fk_on_delete()
    def delete_archived_subject(self, subject_id: UUID, is_archived = True) -> None:
        """Permanently delete an archived subject if there are no dependent entities.
        Args:
            subject_id: ID of subject to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, subject_id, is_archived)
            self.repository.delete_archive(subject_id)

        except EntityNotFoundError as e:
            self.raise_not_found(subject_id, e)
