from typing import List
from uuid import UUID, uuid4

from sqlalchemy.orm import Session
from app.core.curriculum.models.curriculum import AcademicLevelSubject
from app.core.curriculum.services.validators import CurriculumValidator
from app.core.shared.exceptions.database_errors import CompositeDuplicateEntityError
from app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_delete, \
    resolve_fk_on_update
from app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError, UniqueViolationError, \
    DeletionDependencyError
from app.core.shared.exceptions.maps.error_map import error_map


class AcademicLevelSubjectFactory(BaseFactory):
    """Factory class for managing AcademicLevelSubject operations."""

    def __init__(self, session: Session, model = AcademicLevelSubject, current_user = None):
        super().__init__(current_user)
        """Initialize factory.
            Args:
            session: SQLAlchemy db session
            model: Model class, defaults to AcademicLevelSubject
            current_user: The authenticated user performing the operation, if any.
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = CurriculumValidator()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session, current_user)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "AcademicLevelSubject"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_unique_violation({
        "academic_level_subjects_level_id_subject_id_key": ("_", "This subject is already assigned to this level"),
        "academic_level_subjects_code_key": ("name", lambda self, _,  data: data.code)
    })
    @resolve_fk_on_create()
    def create_academic_level_subject(self, level_id: UUID, data) -> AcademicLevelSubject:
        """Create a new AcademicLevelSubject.
        Args:
            level_id: id of the level to be assigned a subject
            data: AcademicLevelSubject data
        Returns:
            AcademicLevelSubject: Created AcademicLevelSubject record
        """

        new_academic_level_subject = AcademicLevelSubject(
            id=uuid4(),
            subject_id=data.subject_id,
            level_id=level_id,
            code=self.validator.validate_code(data.code),
            is_elective=data.is_elective,

            created_by=self.actor_id,
            last_modified_by=self.actor_id
            )
        return self.repository.create(new_academic_level_subject)



    def get_academic_level_subject(self, academic_level_subject_id: UUID) -> AcademicLevelSubject:
        """Get a specific AcademicLevelSubject by ID.
        Args:
            academic_level_subject_id (UUID): ID of AcademicLevelSubject to retrieve
        Returns:
            AcademicLevelSubject: Retrieved AcademicLevelSubject record
        """
        try:
            return self.repository.get_by_id(academic_level_subject_id)
        except EntityNotFoundError as e:
            self.raise_not_found(academic_level_subject_id, e)


    def get_all_academic_level_subjects(self, filters) -> List[AcademicLevelSubject]:
        """Get all active AcademicLevelSubjects with filtering.
        Returns:
            List[AcademicLevelSubject]: List of active AcademicLevelSubjects
        """
        fields = ['is_elective', 'subject_id', 'level_id']
        return self.repository.execute_query(fields, filters)


    @resolve_unique_violation({
        "academic_level_subjects_level_id_subject_id_key": ("_", "This subject is already assigned to this level"),
        "academic_level_subjects_code_key": ("name", lambda self,_,  data: data.code)
    })
    @resolve_fk_on_update()
    def update_subject(self, subject_id: UUID, data: dict) -> AcademicLevelSubject:
        """Update a subject's information.
        Args:
            subject_id (UUID): ID of subject to update
            data (dict): Dictionary containing fields to update
        Returns:
            Subject: Updated subject record
        """
        copied_data = data.copy()
        try:
            existing = self.get_academic_level_subject(subject_id)
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


    def archive_academic_level_subject(self, academic_level_subject_id: UUID, reason) -> AcademicLevelSubject:
        """Archive a AcademicLevelSubject if no active dependencies exist.
        Args:
            academic_level_subject_id (UUID): ID of AcademicLevelSubject to archive
            reason: Reason for archiving
        Returns:
            AcademicLevelSubject: Archived AcademicLevelSubject record
        """
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=academic_level_subject_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=academic_level_subject_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(academic_level_subject_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(academic_level_subject_id, e)


    @resolve_fk_on_delete(display="level subject")
    def delete_academic_level_subject(self, academic_level_subject_id: UUID) -> None:
        """Permanently delete an AcademicLevelSubject if there are no dependent entities
        Args:
            academic_level_subject_id (UUID): ID of AcademicLevelSubject to delete
        """
        try:
            failed_dependencies = self.delete_service.check_active_dependencies_exists(self.model, academic_level_subject_id)

            if failed_dependencies:
                raise DeletionDependencyError(
                    entity_model=self.entity_model, identifier=academic_level_subject_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.delete(academic_level_subject_id)

        except EntityNotFoundError as e:
            self.raise_not_found(academic_level_subject_id, e)


    def get_all_archived_academic_level_subjects(self, filters) -> List[AcademicLevelSubject]:
        """Get all archived AcademicLevelSubjects with filtering.
        Returns:
            List[AcademicLevelSubject]: List of archived AcademicLevelSubject records
        """
        fields = ['is_elective', 'subject_id', 'level_id']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_academic_level_subject(self, academic_level_subject_id: UUID) -> AcademicLevelSubject:
        """Get an archived AcademicLevelSubject by ID.
        Args:
            academic_level_subject_id: ID of AcademicLevelSubject to retrieve
        Returns:
            AcademicLevelSubject: Retrieved AcademicLevelSubject record
        """
        try:
            return self.repository.get_archive_by_id(academic_level_subject_id)
        except EntityNotFoundError as e:
            self.raise_not_found(academic_level_subject_id, e)


    def restore_academic_level_subject(self, academic_level_subject_id: UUID) -> AcademicLevelSubject:
        """Restore an archived AcademicLevelSubject.
        Args:
            academic_level_subject_id: ID of AcademicLevelSubject to restore
        Returns:
            AcademicLevelSubject: Restored AcademicLevelSubject record
        """
        try:
            return self.repository.restore(academic_level_subject_id)
        except EntityNotFoundError as e:
            self.raise_not_found(academic_level_subject_id, e)


    @resolve_fk_on_delete(display="level subject")
    def delete_archived_academic_level_subject(self, academic_level_subject_id: UUID) -> None:
        """Permanently delete an archived AcademicLevelSubject if there are no dependent entities.
        Args:
            academic_level_subject_id: ID of AcademicLevelSubject to delete
        """
        try:
            failed_dependencies = self.delete_service.check_active_dependencies_exists(self.model,academic_level_subject_id)

            if failed_dependencies:
                raise DeletionDependencyError(
                    entity_model=self.entity_model, identifier=academic_level_subject_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            self.repository.delete_archive(academic_level_subject_id)

        except EntityNotFoundError as e:
            self.raise_not_found(academic_level_subject_id, e)
