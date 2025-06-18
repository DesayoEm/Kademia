from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from V2.app.core.curriculum.models.curriculum import StudentSubject
from V2.app.core.curriculum.services.validators import CurriculumValidator
from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError
from V2.app.core.shared.exceptions.maps.error_map import error_map



class StudentSubjectFactory(BaseFactory):
    """Factory class for managing StudentSubject operations."""

    def __init__(self, session: Session, model = StudentSubject, current_user = None):
        super().__init__(current_user)
        """Initialize factory.
            Args:
            session: SQLAlchemy db session
            model: Model class, defaults to StudentSubject
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
        self.domain = "StudentSubject"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )


    @resolve_unique_violation({
        "uq_student_grade_composite": ("student grade", "Check student, subject, and session combination")

    })
    @resolve_fk_on_create()
    def create_student_subject(self, student_id: UUID, data) -> StudentSubject:
        """Create a new StudentSubject.
        Args:
            data: StudentSubject data
            student_id: id of the student to be assigned a subject
        Returns:
            StudentSubject: Created StudentSubject record
        """
        new_student_subject = StudentSubject(
            id=uuid4(),
            student_id=student_id,
            academic_level_subject_id=data.academic_level_subject_id,
            term=data.term,
            academic_session=self.validator.validate_academic_session(data.academic_session),

            created_by=self.actor_id,
            last_modified_by=self.actor_id
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
        fields = ['academic_session', 'term', 'is_active']
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
            return self.repository.archive(student_subject_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(student_subject_id, e)


    @resolve_fk_on_delete()
    def delete_student_subject(self, student_subject_id: UUID, is_archived=False) -> None:
        """Permanently delete an StudentSubject
        Args:
            student_subject_id (UUID): ID of StudentSubject to delete
            is_archived: Whether to check archived or active entities
        """
        try:

            self.repository.delete(student_subject_id)
        except EntityNotFoundError as e:
            self.raise_not_found(student_subject_id, e)


    def get_all_archived_student_subjects(self, filters) -> List[StudentSubject]:
        """Get all archived StudentSubjects with filtering.
        Returns:
            List[StudentSubject]: List of archived StudentSubject records
        """
        fields = ['academic_session', 'term', 'is_active']
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
            self.repository.delete_archive(student_subject_id)

        except EntityNotFoundError as e:
            self.raise_not_found(student_subject_id, e)
