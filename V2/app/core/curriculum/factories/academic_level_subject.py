from typing import List
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from V2.app.core.curriculum.models.curriculum import AcademicLevelSubject
from V2.app.core.curriculum.services.validators import CurriculumValidator
from V2.app.core.shared.exceptions.database_errors import CompositeDuplicateEntityError
from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from V2.app.core.shared.exceptions.maps.error_map import error_map


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
        self.archive_service = ArchiveService(session)
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


    @resolve_fk_on_create()
    def create_academic_level_subject(self, level_id: UUID, data) -> AcademicLevelSubject:
        """Create a new AcademicLevelSubject.
        Args:
            level_id: id of the level to be assigned a subject
            data: AcademicLevelSubject data
        Returns:
            AcademicLevelSubject: Created AcademicLevelSubject record
        """
        try:
            new_academic_level_subject = AcademicLevelSubject(
                id=uuid4(),
                subject_id=data.subject_id,
                level_id=level_id,
                name=self.validator.validate_name(data.name),
                is_elective=data.is_elective,
                academic_session=self.validator.validate_academic_session(data.academic_session),

                created_by=self.actor_id,
                last_modified_by=self.actor_id
            )
            return self.repository.create(new_academic_level_subject)

        except IntegrityError as e:
            if "level_id, subject_id, academic_session" in str(e):
                raise CompositeDuplicateEntityError( #fix.not raised
                    AcademicLevelSubject, str(e),
                    "This subject is already assigned to this level for the specified session"
                )
            raise



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
        fields = ['academic_session', 'is_elective']
        return self.repository.execute_query(fields, filters)

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


    @resolve_fk_on_delete()
    def delete_academic_level_subject(self, academic_level_subject_id: UUID, is_archived=False) -> None:
        """Permanently delete an AcademicLevelSubject if there are no dependent entities
        Args:
            academic_level_subject_id (UUID): ID of AcademicLevelSubject to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, academic_level_subject_id, is_archived)
            return self.repository.delete(academic_level_subject_id)

        except EntityNotFoundError as e:
            self.raise_not_found(academic_level_subject_id, e)


    def get_all_archived_academic_level_subjects(self, filters) -> List[AcademicLevelSubject]:
        """Get all archived AcademicLevelSubjects with filtering.
        Returns:
            List[AcademicLevelSubject]: List of archived AcademicLevelSubject records
        """
        fields = ['academic_session', 'is_elective']
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


    @resolve_fk_on_delete()
    def delete_archived_academic_level_subject(self, academic_level_subject_id: UUID, is_archived = True) -> None:
        """Permanently delete an archived AcademicLevelSubject if there are no dependent entities.
        Args:
            academic_level_subject_id: ID of AcademicLevelSubject to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, academic_level_subject_id, is_archived)
            self.repository.delete_archive(academic_level_subject_id)

        except EntityNotFoundError as e:
            self.raise_not_found(academic_level_subject_id, e)
