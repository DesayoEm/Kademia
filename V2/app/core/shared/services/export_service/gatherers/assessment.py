from typing import Dict, Tuple, Any
from V2.app.core.assessment.models.assessment import Grade, TotalGrade, Repetition

class AssessmentGatherer:
    """Gathers data for assessment entities"""

    @staticmethod
    def gather_grade_data(grade: Grade) -> Tuple[Dict[str, Any], str]:
        """Gather data for Grade entity."""
        file_name = f"Grade_{grade.student_id}_{grade.subject_id}_{grade.academic_year}_{grade.term}_{grade.type}"

        return ({
                    "grade": {
                        "id": str(grade.id),
                        "student_id": str(grade.student_id),
                        "subject_id": str(grade.subject_id),
                        "academic_year": grade.academic_year,
                        "term": grade.term,
                        "type": grade.type,
                        "score": grade.score,
                        "file_url": grade.file_url,
                        "feedback": grade.feedback,
                        "graded_by": str(grade.graded_by),
                        "created_at": grade.created_at,
                        "created_by": str(grade.created_by) if grade.created_by else None,
                        "last_modified_at": grade.last_modified_at,
                        "last_modified_by": str(grade.last_modified_by) if grade.last_modified_by else None,
                        "archived_at": grade.archived_at,
                        "archived_by": str(grade.archived_by) if grade.archived_by else None,
                        "archive_reason": grade.archive_reason,
                    },
                    "student": {
                        "id": str(grade.student.id),
                        "name": f"{grade.student.first_name} {grade.student.last_name}",
                    } if grade.student else None,
                    "subject": {
                        "id": str(grade.subject.id),
                        "name": grade.subject.name,
                    } if grade.subject else None,
                    "grader": {
                        "id": str(grade.grader.id),
                        "name": f"{grade.grader.first_name} {grade.grader.last_name}"
                    } if grade.grader else None
                }, file_name)

    @staticmethod
    def gather_total_grade_data(total_grade: TotalGrade) -> Tuple[Dict[str, Any], str]:
        """Gather data for TotalGrade entity."""
        file_name = f"TotalGrade_{total_grade.student_id}_{total_grade.subject_id}_{total_grade.academic_year}_{total_grade.term}"

        return ({
                    "total_grade": {
                        "id": str(total_grade.id),
                        "student_id": str(total_grade.student_id),
                        "subject_id": str(total_grade.subject_id),
                        "academic_year": total_grade.academic_year,
                        "term": total_grade.term,
                        "total_score": total_grade.total_score,
                        "rank": total_grade.rank,
                        "created_at": total_grade.created_at,
                        "created_by": str(total_grade.created_by) if total_grade.created_by else None,
                        "last_modified_at": total_grade.last_modified_at,
                        "last_modified_by": str(total_grade.last_modified_by) if total_grade.last_modified_by else None,
                        "archived_at": total_grade.archived_at,
                        "archived_by": str(total_grade.archived_by) if total_grade.archived_by else None,
                        "archive_reason": total_grade.archive_reason,
                    },
                    "student": {
                        "id": str(total_grade.student.id),
                        "name": f"{total_grade.student.first_name} {total_grade.student.last_name}"
                    } if total_grade.student else None,
                    "subject": {
                        "id": str(total_grade.subject.id),
                        "name": total_grade.subject.name
                    } if total_grade.subject else None
                }, file_name)

    @staticmethod
    def gather_repetition_data(repetition: Repetition) -> Tuple[Dict[str, Any], str]:
        """Gather data for Repetition entity."""
        file_name = f"Repetition_{repetition.student_id}_{repetition.academic_year}"

        return ({
                    "repetition": {
                        "id": str(repetition.id),
                        "student_id": str(repetition.student_id),
                        "academic_year": repetition.academic_year,
                        "previous_level_id": str(repetition.previous_level_id),
                        "new_level_id": str(repetition.new_level_id),
                        "previous_class_id": str(repetition.previous_class_id),
                        "new_class_id": str(repetition.new_class_id),
                        "reason": repetition.reason,
                        "status": repetition.status,
                        "status_updated_by": str(
                            repetition.status_updated_by) if repetition.status_updated_by else None,
                        "status_updated_at": repetition.status_updated_at,
                        "rejection_reason": repetition.rejection_reason,
                        "created_at": repetition.created_at,
                        "created_by": str(repetition.created_by) if repetition.created_by else None,
                        "last_modified_at": repetition.last_modified_at,
                        "last_modified_by": str(repetition.last_modified_by) if repetition.last_modified_by else None,
                        "archived_at": repetition.archived_at,
                        "archived_by": str(repetition.archived_by) if repetition.archived_by else None,
                        "archive_reason": repetition.archive_reason,
                    },
                    "student": {
                        "id": str(repetition.repeating_student.id),
                        "name": f"{repetition.repeating_student.first_name} {repetition.repeating_student.last_name}"
                    } if repetition.repeating_student else None,
                    "previous_level": {
                        "id": str(repetition.previous_level.id),
                        "name": repetition.previous_level.name
                    } if repetition.previous_level else None,
                    "new_level": {
                        "id": str(repetition.new_level.id),
                        "name": repetition.new_level.name
                    } if repetition.new_level else None,
                    "previous_class": {
                        "id": str(repetition.previous_class.id),
                        "code": repetition.previous_class.code
                    } if repetition.previous_class else None,
                    "new_class": {
                        "id": str(repetition.new_class.id),
                        "code": repetition.new_class.code
                    } if repetition.new_class else None,
                    "status_updated_by": {
                        "id": str(repetition.status_updated_staff.id),
                        "name": f"{repetition.status_updated_staff.first_name} {repetition.status_updated_staff.last_name}"
                    } if repetition.status_updated_staff else None
                }, file_name)

