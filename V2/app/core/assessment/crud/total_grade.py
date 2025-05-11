from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.assessment.models.assessment import TotalGrade
from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.assessment.schemas.total_grade import (
    TotalGradeFilterParams, TotalGradeCreate, TotalGradeResponse,
)
from V2.app.core.assessment.factories.total_grade import TotalGradeFactory
from V2.app.core.shared.services.export_service.export import ExportService


class TotalGradeCrud:
    """CRUD operations for total grades."""

    def __init__(self, session: Session, current_user = None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.current_user = current_user
        self.factory = TotalGradeFactory(session, current_user=current_user)
        self.export_service = ExportService(session)


    def create_total_grade(self, student_subject_id: UUID) -> TotalGradeResponse:
        """Create a new total grade."""
        total_grade = self.factory.create_total_grade(student_subject_id)
        return TotalGradeResponse.model_validate(total_grade)


    def get_total_grade(self, total_grade_id: UUID) -> TotalGradeResponse:
        """Get total grade by ID."""
        total_grade = self.factory.get_total_grade(total_grade_id)
        return TotalGradeResponse.model_validate(total_grade)


    def get_all_total_grades(self, filters:TotalGradeFilterParams) -> List[TotalGradeResponse]:
        """Get all active total grades."""
        total_grades = self.factory.get_all_total_grades(filters)
        return [TotalGradeResponse.model_validate(total_grade) for total_grade in total_grades]


    def archive_total_grade(self, total_grade_id: UUID, reason: ArchiveReason) -> None:
        """Archive a total grade.
        Args:
            total_grade_id: total grade UUID
            reason: Reason for archiving
        Returns:
            TotalGradeResponse: Archived total grade
        """
        self.factory.archive_total_grade(total_grade_id, reason)


    def export_total_grade(self, total_grade_id: UUID, export_format: str) -> str:
        """Export total grade and its associated data
        Args:
            total_grade_id: total grade UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            TotalGrade, total_grade_id, export_format
        )


    def delete_total_grade(self, total_grade_id: UUID) -> None:
        """Permanently delete a total grade."""
        self.factory.delete_total_grade(total_grade_id)


    # Archived total grade operations
    def get_archived_total_grade(self, total_grade_id: UUID) -> TotalGradeResponse:
        """Get an archived total grade by ID."""
        total_grade = self.factory.get_archived_total_grade(total_grade_id)
        return TotalGradeResponse.model_validate(total_grade)


    def get_all_archived_total_grades(self, filters: TotalGradeFilterParams) -> List[TotalGradeResponse]:
        """Get all archived total grades."""
        total_grades = self.factory.get_all_archived_total_grades(filters)
        return [TotalGradeResponse.model_validate(total_grade) for total_grade in total_grades]


    def restore_total_grade(self, total_grade_id: UUID) -> TotalGradeResponse:
        """Restore an archived total grade."""
        total_grade = self.factory.restore_total_grade(total_grade_id)
        return TotalGradeResponse.model_validate(total_grade)


    def delete_archived_total_grade(self, total_grade_id: UUID) -> None:
        """Permanently delete an archived total grade."""
        self.factory.delete_archived_total_grade(total_grade_id)