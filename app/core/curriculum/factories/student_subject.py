from typing import List
from uuid import UUID, uuid4

from sqlalchemy.orm import Session
from app.core.curriculum.models.curriculum import StudentSubject
from app.core.curriculum.services.curriculum_service import CurriculumService
from app.core.curriculum.services.validators import CurriculumValidator
from app.core.shared.exceptions.database_errors import CompositeDuplicateEntityError
from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_delete
from app.core.shared.exceptions import EntityNotFoundError, UniqueViolationError
from app.core.shared.exceptions.maps.error_map import error_map



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
        self.session = session
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = CurriculumValidator()
        self.service = CurriculumService(session, current_user)
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


    @resolve_fk_on_create()
    def create_student_subject(self, student_id: UUID, data) -> StudentSubject:
        """Create a new StudentSubject.
        Args:
            data: StudentSubject data
            student_id: id of the student to be assigned a subject
        Returns:
            StudentSubject: Created StudentSubject record
        """
        from app.core.curriculum.factories.academic_level_subject import AcademicLevelSubjectFactory
        from app.core.academic_structure.models import AcademicLevelSubject
        academic_factory = AcademicLevelSubjectFactory(self.session, AcademicLevelSubject, self.current_user)
        level_subject = academic_factory.get_academic_level_subject(data.academic_level_subject_id)
        level_id = level_subject.level_id
        try:
            new_student_subject = StudentSubject(
                id=uuid4(),
                student_id=student_id,
                academic_level_subject_id=self.service.check_academic_level(
                    student_id, level_id, data.academic_level_subject_id
                ),
                term=data.term,
                academic_session=self.validator.validate_academic_session(data.academic_session),

                created_by=self.actor_id,
                last_modified_by=self.actor_id
            )
            return self.repository.create(new_student_subject)

        except UniqueViolationError as e:
            if "student_subjects_student_id_academic_level_subject_id_acade_key" in str(e):
                raise CompositeDuplicateEntityError( #fix.not raised
                    StudentSubject, str(e),
                    "This subject is already assigned to this student for the specified session"
                )
            raise


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
        fields = ['academic_session', 'term', 'is_active','student_id', 'academic_level_subject_id']
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
    def delete_student_subject(self, student_subject_id: UUID) -> None:
        """Permanently delete an StudentSubject
        Args:
            student_subject_id (UUID): ID of StudentSubject to delete
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
        fields = ['academic_session', 'term', 'is_active','student_id', 'academic_level_subject_id']
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
    def delete_archived_student_subject(self, student_subject_id: UUID) -> None:
        """Permanently delete an archived StudentSubject if there are no dependent entities.
        Args:
            student_subject_id: ID of StudentSubject to delete
        """
        try:
            self.repository.delete_archive(student_subject_id)

        except EntityNotFoundError as e:
            self.raise_not_found(student_subject_id, e)
