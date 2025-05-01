from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from V2.app.core.curriculum.models.curriculum import AcademicLevelSubject
from V2.app.core.curriculum.validators import CurriculumValidator
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from V2.app.core.shared.exceptions.maps.error_map import error_map

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class AcademicLevelSubjectFactory:
    """Factory class for managing AcademicLevelSubject operations."""

    def __init__(self, session: Session, model = AcademicLevelSubject):
        """Initialize factory with model and db session.
            Args:
            session: SQLAlchemy db session
            model: Model class, defaults to AcademicLevelSubject
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = CurriculumValidator()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.domain = "AcademicLevelSubject"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )


    @resolve_unique_violation({
        "trig to find out": ("name", lambda self, data: data.name)
    })
    @resolve_fk_on_create()
    def create_academic_level_subject(self, data) -> AcademicLevelSubject:
        """Create a new AcademicLevelSubject.
        Args:
            data: AcademicLevelSubject data
        Returns:
            AcademicLevelSubject: Created AcademicLevelSubject record
        """
        new_academic_level_subject = AcademicLevelSubject(
            id=uuid4(),
            student_id=data.student_id,
            subject_id=data.subject_id,
            is_elective=data.is_elective,
            department_id=data.department_id,
            session_year=self.validator.validate_session_start_year(data.session_year),

            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID
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
        fields = ['session_year', 'level_id', 'subject_id', 'educator_id']
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
            return self.repository.archive(academic_level_subject_id, SYSTEM_USER_ID, reason)

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
        fields = ['session_year', 'level_id', 'subject_id', 'educator_id']
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
