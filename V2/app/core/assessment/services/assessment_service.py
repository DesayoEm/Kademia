from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from V2.app.core.assessment.models.assessment import TotalGrade
from V2.app.core.shared.services.audit_export_service.export import ExportService
from V2.app.core.shared.exceptions.assessment_errors import WeightTooHighError
from V2.app.core.shared.exceptions import InvalidWeightError
from V2.app.core.assessment.models.assessment import Grade


class AssessmentService:
    def __init__(self, session: Session):
        self.session = session
        self.export_service = ExportService(session)

    def validate_grade_weight(self, value: int, student_subject_id: UUID) -> int:

        """Ensure cumulative weight for a term doesn't exceed 10."""
        if value > 10:
            raise WeightTooHighError(entry=value)

        stmt = select(func.coalesce(func.sum(Grade.weight), 0)).where(
            Grade.student_subject_id == student_subject_id
        )
        cumulative = self.session.scalar(stmt)

        if value + cumulative > 10:
            raise InvalidWeightError(
                entry=value, cumulative_weight=cumulative
            )
        return value


    def validate_grade_weight_on_update(self, current_value: int, new_value: int, student_subject_id: UUID) -> int:

        """Ensure cumulative weight for a term doesn't exceed 10 on update."""
        if new_value > 10:
            raise WeightTooHighError(entry=new_value)

        stmt = select(func.coalesce(func.sum(Grade.weight), 0)).where(
            Grade.student_subject_id == student_subject_id
        )
        cumulative = self.session.scalar(stmt)


        if new_value + cumulative - current_value > 10:
            raise InvalidWeightError(
                entry=new_value, cumulative_weight=cumulative
            )
        return new_value


    def calculate_total_grade(self, student_subject_id):
        """Calculate total grade from all the grades for a student subject"""
        total_weight_stmt  = select(func.sum(Grade.weight).where(
            Grade.student_subject_id == student_subject_id,
        ))
        total_weight = self.session.scalar(total_weight_stmt)

        weighted_score_stmt = select(func.sum(
            (Grade.score/Grade.max_score)*Grade.weight
            )).where(
                Grade.student_subject_id == student_subject_id,
    )
        weighted_score = self.session.scalar(weighted_score_stmt)

        total_grade = (weighted_score / total_weight) * 100
        return round(total_grade, 2)


    def export_grade_audit(self, grade_id: UUID, export_format: str) -> str:
        """Export grade and its associated data
        Args:
            grade_id: grade UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Grade, grade_id, export_format
        )


    def export_total_grade_audit(self, total_grade_id: UUID, export_format: str) -> str:
        """Export total grade and its associated data
        Args:
            total_grade_id: grade UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            TotalGrade, total_grade_id, export_format
        )