from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from V2.app.core.assessment.models.assessment import TotalGrade
from V2.app.core.assessment.services.assessment_service import AssessmentService
from V2.app.core.assessment.services.validators import AssessmentValidator
from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError
from V2.app.core.shared.exceptions.maps.error_map import error_map


class TotalGradeFactory(BaseFactory):
    """Factory class for managing TotalGrade operations."""

    def __init__(self, session: Session, model=TotalGrade, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session, model and current user.
        Args:
            session: SQLAlchemy db session
            model: Model class, defaults to TotalGrade
            current_user: The authenticated user performing the operation, if any.
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = AssessmentValidator(session)
        self.service = AssessmentService(session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "TotalGrade"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    def create_total_grade(self, student_id: UUID, student_subject_id:UUID) -> TotalGrade:
        """Create a new TotalGrade.
        Args:
            student_id: id of the student to grade
            student_subject_id: id of the subject to grade
        Returns:
            TotalGrade: Created TotalGrade record
        """
        new_total_grade = TotalGrade(
            id=uuid4(),
            student_subject_id=student_subject_id,
            student_id=student_id,
            total_score=self.service.calculate_total_grade(
                student_subject_id
            ),
            created_by=self.actor_id,
            last_modified_by=self.actor_id
        )
        
        return self.repository.create(new_total_grade)


    def get_total_grade(self, total_grade_id: UUID) -> TotalGrade:
        """Get a specific TotalGrade by ID.
        Args:
            total_grade_id (UUID): ID of TotalGrade to retrieve
        Returns:
            TotalGrade: Retrieved TotalGrade record
        """
        try:
            return self.repository.get_by_id(total_grade_id)
        except EntityNotFoundError as e:
            self.raise_not_found(total_grade_id, e)


    def get_all_total_grades(self, filters) -> List[TotalGrade]:
        """Get all active TotalGrades with filtering.
        Returns:
            List[TotalGrade]: List of active TotalGrades
        """
        fields = ['academic_session', 'term']
        return self.repository.execute_query(fields, filters)


    def archive_total_grade(self, total_grade_id: UUID, reason) -> TotalGrade:
        """Archive a TotalGrade record.
        Args:
            total_grade_id (UUID): ID of TotalGrade to archive
            reason: Reason for archiving
        Returns:
            TotalGrade: Archived TotalGrade record
        """
        try:
            return self.repository.archive(total_grade_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(total_grade_id, e)

    @resolve_fk_on_delete()
    def delete_total_grade(self, total_grade_id: UUID) -> None:
        """Permanently delete a TotalGrade
        Args:
            total_grade_id (UUID): ID of TotalGrade to delete
        """
        try:
            return self.repository.delete(total_grade_id)

        except EntityNotFoundError as e:
            self.raise_not_found(total_grade_id, e)


    def get_all_archived_total_grades(self, filters) -> List[TotalGrade]:
        """Get all archived TotalGrades with filtering.
        Returns:
            List[TotalGrade]: List of archived TotalGrade records
        """
        fields = ['academic_session', 'term']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_total_grade(self, total_grade_id: UUID) -> TotalGrade:
        """Get an archived TotalGrade by ID.
        Args:
            total_grade_id: ID of TotalGrade to retrieve
        Returns:
            TotalGrade: Retrieved TotalGrade record
        """
        try:
            return self.repository.get_archive_by_id(total_grade_id)
        except EntityNotFoundError as e:
            self.raise_not_found(total_grade_id, e)


    def restore_total_grade(self, total_grade_id: UUID) -> TotalGrade:
        """Restore an archived TotalGrade.
        Args:
            total_grade_id: ID of TotalGrade to restore
        Returns:
            TotalGrade: Restored TotalGrade record
        """
        try:
            return self.repository.restore(total_grade_id)
        except EntityNotFoundError as e:
            self.raise_not_found(total_grade_id, e)


    @resolve_fk_on_delete()
    def delete_archived_total_grade(self, total_grade_id: UUID) -> None:
        """Permanently delete an archived TotalGrade.
        Args:
            total_grade_id: ID of TotalGrade to delete
        """
        try:
            self.repository.delete_archive(total_grade_id)

        except EntityNotFoundError as e:
            self.raise_not_found(total_grade_id, e)
