from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from V2.app.core.assessment.models.assessment import Grade
from V2.app.core.assessment.services.validators import AssessmentValidator
from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.core.shared.validators.entity_validators import EntityValidator
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError
from V2.app.core.shared.exceptions.maps.error_map import error_map


class GradeFactory(BaseFactory):
    """Factory class for managing Grade operations."""

    def __init__(self, session: Session, model = Grade, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session, model and current user.
        Args:
            session: SQLAlchemy db session
            model: Model class, defaults to Grade
            current_user: The authenticated user performing the operation, if any.
        """
        self.model = model
        self.session = session
        self.current_user = current_user
        self.repository = SQLAlchemyRepository(self.model, session)
        self.entity_validator = EntityValidator(session)
        self.validator = AssessmentValidator(session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Grade"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    def create_grade(self, student_id:UUID, student_subject_id:UUID,  data) -> Grade:
        """Create a new Grade.
        Args:
            student_id: id of the student to grade
            student_subject_id: id of the student subject to grade
            data: Grade data
        Returns:
            Grade: Created Grade record
        """
        from V2.app.core.assessment.services.assessment_service import AssessmentService
        service = AssessmentService(self.session)

        new_grade = Grade(
            id=uuid4(),
            student_id=student_id,
            student_subject_id=student_subject_id,
            academic_session=self.validator.validate_academic_session(data.academic_session),
            term=data.term,
            max_score=self.validator.validate_max_score(data.max_score),
            score=self.validator.validate_score(data.max_score, data.score),
            weight=service.validate_grade_weight(
                data.weight, student_subject_id
            ),
            type=data.type,
            graded_by =  self.entity_validator.validate_staff_exists(data.graded_by),
            graded_on=self.validator.validate_graded_date(data.graded_on),
      
            created_by=self.actor_id,
            last_modified_by=self.actor_id
        )
        return self.repository.create(new_grade)


    def get_grade(self, grade_id: UUID) -> Grade:
        """Get a specific Grade by ID.
        Args:
            grade_id (UUID): ID of Grade to retrieve
        Returns:
            Grade: Retrieved Grade record
        """
        try:
            return self.repository.get_by_id(grade_id)
        except EntityNotFoundError as e:
            self.raise_not_found(grade_id, e)


    def get_all_grades(self, filters) -> List[Grade]:
        """Get all active Grades with filtering.
        Returns:
            List[Grade]: List of active Grades
        """
        fields = ['type', 'academic_session', 'term', 'graded_on']
        return self.repository.execute_query(fields, filters)


    @resolve_fk_on_update()
    def update_grade(self, grade_id: UUID, data: dict) -> Grade:
        """Update a Grade's information.
        Args:
            grade_id (UUID): ID of Grade to update
            data (dict): Dictionary containing fields to update
        Returns:
            Grade: Updated Grade record
        """
        from V2.app.core.assessment.services.assessment_service import AssessmentService
        service = AssessmentService(self.session)

        copied_data = data.copy()
        to_be_validated = ["score", "max_score", "academic_session", "weight", "graded_on"]
        try:
            existing = self.get_grade(grade_id)
            for key, value in copied_data.items():
                if hasattr(existing, key) and key not in to_be_validated:
                    setattr(existing, key, value)

            if "academic_session" in data:
                updated_academic_session = self.validator.validate_academic_session(data.academic_session)
                setattr(existing, "academic_session", updated_academic_session)

            if "graded_on" in data:
                updated_graded_on = self.validator.validate_graded_date(data.graded_on)
                setattr(existing, "graded_on", updated_graded_on)

            if "weight" in data:
                current_weight = existing.weight
                existing.weight = service.validate_grade_weight_on_update(
                    current_weight, data.get('weight'), existing.student_subject_id
                )

            if "score" in data:
                max_score = (
                    self.validator.validate_max_score(data.max_score)
                    if "max_score" in data
                    else existing.max_score
                )
                validated_score = self.validator.validate_score(max_score, data.score)
                setattr(existing, "score", validated_score)

            return self.repository.update(grade_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
                self.raise_not_found(grade_id, e)


    def archive_grade(self, grade_id: UUID, reason) -> Grade:
        """Archive a Grade record.
        Args:
            grade_id (UUID): ID of Grade to archive
            reason: Reason for archiving
        Returns:
            Grade: Archived Grade record
        """
        try:
            return self.repository.archive(grade_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(grade_id, e)


    @resolve_fk_on_delete()
    def delete_grade(self, grade_id: UUID, is_archived=False) -> None:
        """Permanently delete a Grade
        Args:
            grade_id (UUID): ID of Grade to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            return self.repository.delete(grade_id)

        except EntityNotFoundError as e:
            self.raise_not_found(grade_id, e)


    def get_all_archived_grades(self, filters) -> List[Grade]:
        """Get all archived Grades with filtering.
        Returns:
            List[Grade]: List of archived Grade records
        """
        fields = ['type', 'academic_session', 'term', 'graded_on']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_grade(self, grade_id: UUID) -> Grade:
        """Get an archived Grade by ID.
        Args:
            grade_id: ID of Grade to retrieve
        Returns:
            Grade: Retrieved Grade record
        """
        try:
            return self.repository.get_archive_by_id(grade_id)
        except EntityNotFoundError as e:
            self.raise_not_found(grade_id, e)


    def restore_grade(self, grade_id: UUID) -> Grade:
        """Restore an archived Grade.
        Args:
            grade_id: ID of Grade to restore
        Returns:
            Grade: Restored Grade record
        """
        try:
            return self.repository.restore(grade_id)
        except EntityNotFoundError as e:
            self.raise_not_found(grade_id, e)


    @resolve_fk_on_delete()
    def delete_archived_grade(self, grade_id: UUID, is_archived = True) -> None:
        """Permanently delete an archived Grade.
        Args:
            grade_id: ID of Grade to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.repository.delete_archive(grade_id)

        except EntityNotFoundError as e:
            self.raise_not_found(grade_id, e)
