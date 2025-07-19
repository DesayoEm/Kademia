from typing import Dict, Tuple, Any
from app.core.assessment.models.assessment import Grade, TotalGrade

class AssessmentGatherer:
    """Gathers data for assessment entities"""

    @staticmethod
    def gather_grade_data(grade: Grade) -> Tuple[Dict[str, Any], str]:
        """Gather data for Grade entity."""
        file_name = f"Grade_{grade.student_id}_{grade.subject_id}_{grade.academic_session}_{grade.term}_{grade.type}"

        return ({
                    "grade": {
                        "id": str(grade.id),
                        "student_id": str(grade.student_id),
                        "subject_id": str(grade.subject_id),
                        "academic_session": grade.academic_session,
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
        file_name = f"TotalGrade_{total_grade.student_id}_{total_grade.subject_id}_{total_grade.academic_session}_{total_grade.term}"

        return ({
                    "total_grade": {
                        "id": str(total_grade.id),
                        "student_id": str(total_grade.student_id),
                        "subject_id": str(total_grade.subject_id),
                        "academic_session": total_grade.academic_session,
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


