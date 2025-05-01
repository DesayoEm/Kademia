from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from V2.app.core.curriculum.models.curriculum import StudentSubject
from V2.app.core.curriculum.validators import CurriculumValidator
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from V2.app.core.shared.exceptions.maps.error_map import error_map

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class StudentSubjectFactory:
    """Factory class for managing StudentSubject operations."""

    def __init__(self, session: Session, model = StudentSubject):
        """Initialize factory with model and db session.
            Args:
            session: SQLAlchemy db session
            model: Model class, defaults to StudentSubject
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = CurriculumValidator()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.domain = "StudentSubject"

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
    def create_student_subject(self, data) -> StudentSubject:
        """Create a new StudentSubject.
        Args:
            data: StudentSubject data
        Returns:
            StudentSubject: Created StudentSubject record
        """
        new_student_subject = StudentSubject(
            id=uuid4(),
            student_id=data.student_id,
            subject_id=data.subject_id,
            term=data.term,
            session_year=self.validator.validate_session_start_year(data.session_year),

            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID
        )
        return self.repository.create(new_student_subject)


    def get_student_subject(self, student_subject_id: UUID) -> StudentSubject:
        """Get a specific StudentSubject by ID.
        Args:
            student_subject_id (UUID): ID of StudentSubject to retrieve
        Returns:
            StudentSubject: Retrieved StudentSubject record
        """
        try:
            return self.repository.get_by_id(student_subject_id)
        except EntityNotFoundError as e:
            self.raise_not_found(student_subject_id, e)


    def get_all_student_subjects(self, filters) -> List[StudentSubject]:
        """Get all active StudentSubjects with filtering.
        Returns:
            List[StudentSubject]: List of active StudentSubjects
        """
        fields = ['subject_id', 'session_year', 'level_id', 'student_id']
        return self.repository.execute_query(fields, filters)

    def archive_student_subject(self, student_subject_id: UUID, reason) -> StudentSubject:
        """Archive a StudentSubject if no active dependencies exist.
        Args:
            student_subject_id (UUID): ID of StudentSubject to archive
            reason: Reason for archiving
        Returns:
            StudentSubject: Archived StudentSubject record
        """
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=student_subject_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=student_subject_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(student_subject_id, SYSTEM_USER_ID, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(student_subject_id, e)


    @resolve_fk_on_delete()
    def delete_student_subject(self, student_subject_id: UUID, is_archived=False) -> None:
        """Permanently delete an StudentSubject if there are no dependent entities
        Args:
            student_subject_id (UUID): ID of StudentSubject to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, student_subject_id, is_archived)
            return self.repository.delete(student_subject_id)

        except EntityNotFoundError as e:
            self.raise_not_found(student_subject_id, e)


    def get_all_archived_student_subjects(self, filters) -> List[StudentSubject]:
        """Get all archived StudentSubjects with filtering.
        Returns:
            List[StudentSubject]: List of archived StudentSubject records
        """
        fields = ['subject_id', 'session_year', 'level_id', 'student_id']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_student_subject(self, student_subject_id: UUID) -> StudentSubject:
        """Get an archived StudentSubject by ID.
        Args:
            student_subject_id: ID of StudentSubject to retrieve
        Returns:
            StudentSubject: Retrieved StudentSubject record
        """
        try:
            return self.repository.get_archive_by_id(student_subject_id)
        except EntityNotFoundError as e:
            self.raise_not_found(student_subject_id, e)


    def restore_student_subject(self, student_subject_id: UUID) -> StudentSubject:
        """Restore an archived StudentSubject.
        Args:
            student_subject_id: ID of StudentSubject to restore
        Returns:
            StudentSubject: Restored StudentSubject record
        """
        try:
            return self.repository.restore(student_subject_id)
        except EntityNotFoundError as e:
            self.raise_not_found(student_subject_id, e)


    @resolve_fk_on_delete()
    def delete_archived_student_subject(self, student_subject_id: UUID, is_archived = True) -> None:
        """Permanently delete an archived StudentSubject if there are no dependent entities.
        Args:
            student_subject_id: ID of StudentSubject to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, student_subject_id, is_archived)
            self.repository.delete_archive(student_subject_id)

        except EntityNotFoundError as e:
            self.raise_not_found(student_subject_id, e)
