from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.assessment.models.assessment import Grade
from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.assessment.schemas.grade import (
    GradeCreate, GradeUpdate, GradeResponse, GradeFilterParams
)
from V2.app.core.assessment.factories.grade import GradeFactory
from V2.app.core.shared.services.export_service.export import ExportService


class GradeCrud:
    """CRUD operations for grades."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
        """
        self.session = session
        self.factory = GradeFactory(session)
        self.export_service = ExportService(session)


    def create_grade(self, data: GradeCreate) -> GradeResponse:
        """Create a new grade.
        Args:
            data: Validated grade creation data
        Returns:
            GradeResponse: Created grade
        """
        grade = self.factory.create_grade(data)
        return GradeResponse.model_validate(grade)


    def get_grade(self, grade_id: UUID) -> GradeResponse:
        """Get grade by ID.
        Args:
            grade_id: grade UUID
        Returns:
            GradeResponse: Retrieved grade
        """
        grade = self.factory.get_grade(grade_id)
        return GradeResponse.model_validate(grade)


    def get_all_grades(self, filters: GradeFilterParams) -> List[GradeResponse]:
        """Get all active grades.
        Returns:
            List[GradeResponse]: List of active grades
        """
        grades = self.factory.get_all_grades(filters)
        return [GradeResponse.model_validate(grade) for grade in grades]


    def update_grade(self, grade_id: UUID, data: GradeUpdate) -> GradeResponse:
        """Update grade information.
        Args:
            grade_id: grade UUID
            data: Validated update data
        Returns:
            GradeResponse: Updated grade
        """
        data = data.model_dump(exclude_unset=True)
        updated_grade = self.factory.update_grade(grade_id, data)
        return GradeResponse.model_validate(updated_grade)


    def archive_grade(self, grade_id: UUID, reason: ArchiveReason) -> None:
        """Archive a grade.
        Args:
            grade_id: grade UUID
            reason: Reason for archiving
        Returns:
            GradeResponse: Archived grade
        """
        self.factory.archive_grade(grade_id, reason)


    def export_grade(self, grade_id: UUID, export_format: str) -> str:
        """Export grade and its associated data
        Args:
            grade_id: grade UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Grade, grade_id, export_format
        )


    def delete_grade(self, grade_id: UUID) -> None:
        """Permanently delete a grade.
        Args:
            grade_id: grade UUID
        """
        self.factory.delete_grade(grade_id)


    # Archived grade operations
    def get_archived_grade(self, grade_id: UUID) -> GradeResponse:
        """Get an archived grade by ID.
        Args:
            grade_id: grade UUID
        Returns:
            GradeResponse: Retrieved archived grade
        """
        grade = self.factory.get_archived_grade(grade_id)
        return GradeResponse.model_validate(grade)

    def get_all_archived_grades(self, filters: GradeFilterParams) -> List[GradeResponse]:
        """Get all archived grades.
        Args:
            filters: Filter parameters
        Returns:
            List[GradeResponse]: List of archived grades
        """
        grades = self.factory.get_all_archived_grades(filters)
        return [GradeResponse.model_validate(grade) for grade in grades]


    def restore_grade(self, grade_id: UUID) -> GradeResponse:
        """Restore an archived grade.
        Args:
            grade_id: grade UUID
        Returns:
            GradeResponse: Restored grade
        """
        grade = self.factory.restore_grade(grade_id)
        return GradeResponse.model_validate(grade)


    def delete_archived_grade(self, grade_id: UUID) -> None:
        """Permanently delete an archived grade.
        Args:
            grade_id: grade UUID
        """
        self.factory.delete_archived_grade(grade_id)