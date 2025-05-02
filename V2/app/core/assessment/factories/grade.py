from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from V2.app.core.assessment.models.assessment import Grade
from V2.app.core.assessment.validators import AssessmentValidator
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError
from V2.app.core.shared.exceptions.maps.error_map import error_map

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class GradeFactory:
    """Factory class for managing Grade operations."""

    def __init__(self, session: Session, model = Grade):
        """Initialize factory with model and db session.
            Args:
            session: SQLAlchemy db session
            model: Model class, defaults to Grade
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = AssessmentValidator()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.domain = "Grade"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    def create_grade(self, data) -> Grade:
        """Create a new Grade.
        Args:
            data: Grade data
        Returns:
            Grade: Created Grade record
        """
        new_grade = Grade(
            id=uuid4(),
            session_year=self.validator.validate_session_year(data.session_year),
            term=data.term,
            max_score=self.validator.validate_max_score(data.score),
            score=self.validator.validate_score(data.max_score, data.score),
            weight=self.validator.vvvv(data.weight),
            type=data.type,
            graded_by =  data.graded_by,
            graded_on=self.validator.validate_graded_date(data.graded_on),
      
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID
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
        fields = ['name', 'session_year', 'term', 'graded_on']
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
        copied_data = data.copy()
        try:
            existing = self.get_grade(grade_id)
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

            existing.last_modified_by = SYSTEM_USER_ID
            return self.repository.update(grade_id, existing)

        except EntityNotFoundError as e:
                self.raise_not_found(grade_id, e)


    def archive_grade(self, grade_id: UUID, reason) -> Grade:
        """Archive a Grade if no active dependencies exist.
        Args:
            grade_id (UUID): ID of Grade to archive
            reason: Reason for archiving
        Returns:
            Grade: Archived Grade record
        """
        try:
            return self.repository.archive(grade_id, SYSTEM_USER_ID, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(grade_id, e)


    @resolve_fk_on_delete()
    def delete_grade(self, grade_id: UUID, is_archived=False) -> None:
        """Permanently delete a Grade if there are no dependent entities
        Args:
            grade_id (UUID): ID of Grade to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, grade_id, is_archived)
            return self.repository.delete(grade_id)

        except EntityNotFoundError as e:
            self.raise_not_found(grade_id, e)

    def get_all_archived_grades(self, filters) -> List[Grade]:
        """Get all archived Grades with filtering.
        Returns:
            List[Grade]: List of archived Grade records
        """
        fields = ['name']
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
        """Permanently delete an archived Grade if there are no dependent entities.
        Args:
            grade_id: ID of Grade to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, grade_id, is_archived)
            self.repository.delete_archive(grade_id)

        except EntityNotFoundError as e:
            self.raise_not_found(grade_id, e)
