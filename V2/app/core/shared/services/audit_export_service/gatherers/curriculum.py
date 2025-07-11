from typing import Dict, Tuple, Any
from V2.app.core.curriculum.models.curriculum import (
    Subject, AcademicLevelSubject, StudentSubject, SubjectEducator
)


class CurriculumGatherer:
    """Gathers data for curriculum entities"""

    @staticmethod
    def gather_subject_data(subject: Subject) -> Tuple[Dict[str, Any], str]:
        """Gather data for Subject entity."""
        file_name = f"Subject_{subject.name}"

        return ({
            "subject": {
                "id": str(subject.id),
                "name": subject.name,
                "department_id": str(subject.department_id),
                "created_at": subject.created_at,
                "created_by": str(subject.created_by) if subject.created_by else None,
                "last_modified_at": subject.last_modified_at,
                "last_modified_by": str(subject.last_modified_by) if subject.last_modified_by else None,
                "archived_at": subject.archived_at,
                "archived_by": str(subject.archived_by) if subject.archived_by else None,
                "archive_reason": subject.archive_reason,
            },
            "educators_assigned": [
                {
                    "id": str(educator.id),
                    "level_id": str(educator.level_id),
                    "educator_id": str(educator.educator_id),
                    "academic_session": educator.academic_session,
                    "term": educator.term,
                    "is_active": educator.is_active,
                    "date_assigned": educator.date_assigned
                } for educator in subject.educators
            ],
            "academic_levels": [
                {
                    "id": str(al.id),
                    "level_id": str(al.level_id),
                    "educator_id": str(al.educator_id),
                    "academic_session": al.academic_session,
                    "is_elective": al.is_elective,
                    "curriculum_url": al.curriculum_url
                } for al in subject.academic_levels
            ],
            "student_enrollments": [
                {
                    "id": str(ss.id),
                    "student_id": str(ss.student_id),
                    "academic_session": ss.academic_session,
                    "term": ss.term,
                    "is_active": ss.is_active
                } for ss in subject.students
            ],
            "grades": [
                {
                    "id": str(g.id),
                    "student_id": str(g.student_id),
                    "term": g.term,
                    "type": g.type,
                    "score": g.score,
                    "graded_by": str(g.graded_by),
                    "academic_year": g.academic_session,
                    "file_url": g.file_url,
                    "feedback": g.feedback
                } for g in subject.grades
            ],
            "total_grades": [
                {
                    "id": str(tg.id),
                    "student_id": str(tg.student_id),
                    "term": tg.term,
                    "total_score": tg.total_score,
                    "rank": tg.rank,
                    "academic_year": tg.academic_session
                } for tg in subject.total_grades
            ]
        }, file_name)

    @staticmethod
    def gather_academic_level_subject_data(entry: AcademicLevelSubject) -> Tuple[Dict[str, Any], str]:
        """Gather data for AcademicLevelSubject entity."""
        file_name = f"AcademicLevelSubject_{entry.subject_id}_{entry.level_id}_{entry.academic_session}"

        return ({
                    "academic_level_subject": {
                        "id": str(entry.id),
                        "level_id": str(entry.level_id),
                        "subject_id": str(entry.subject_id),
                        "educator_id": str(entry.educator_id),
                        "academic_year": entry.academic_session,
                        "is_elective": entry.is_elective,
                        "curriculum_url": entry.curriculum_url,
                        "created_at": entry.created_at,
                        "created_by": str(entry.created_by) if entry.created_by else None,
                        "last_modified_at": entry.last_modified_at,
                        "last_modified_by": str(entry.last_modified_by) if entry.last_modified_by else None,
                        "archived_at": entry.archived_at,
                        "archived_by": str(entry.archived_by) if entry.archived_by else None,
                        "archive_reason": entry.archive_reason,
                    },
                    "level": {
                        "id": str(entry.level.id),
                        "name": entry.level.name,
                        "description": entry.level.description,
                        "order": entry.level.order
                    } if entry.level else None,
                    "subject": {
                        "id": str(entry.subject.id),
                        "name": entry.subject.name,
                        "department_id": str(entry.subject.department_id),

                    } if entry.subject else None
                }, file_name)


    @staticmethod
    def gather_student_subject_data(enrollment: StudentSubject) -> Tuple[Dict[str, Any], str]:
        """Gather data for StudentSubject entity."""
        file_name = f"StudentSubject_{enrollment.student_id}_{enrollment.subject_id}_{enrollment.academic_session}_{enrollment.term}"

        return ({
                    "student_subject": {
                        "id": str(enrollment.id),
                        "student_id": str(enrollment.student_id),
                        "subject_id": str(enrollment.subject_id),
                        "academic_year": enrollment.academic_session,
                        "term": enrollment.term,
                        "is_active": enrollment.is_active,
                        "created_at": enrollment.created_at,
                        "created_by": str(enrollment.created_by) if enrollment.created_by else None,
                        "last_modified_at": enrollment.last_modified_at,
                        "last_modified_by": str(enrollment.last_modified_by) if enrollment.last_modified_by else None,
                        "archived_at": enrollment.archived_at,
                        "archived_by": str(enrollment.archived_by) if enrollment.archived_by else None,
                        "archive_reason": enrollment.archive_reason,
                    },
                    "student": {
                        "id": str(enrollment.student.id),
                        "name": f"{enrollment.student.first_name} {enrollment.student.last_name}"
                    } if enrollment.student else None,
                    "subject": {
                        "id": str(enrollment.subject.id),
                        "name": enrollment.subject.name
                    } if enrollment.subject else None
                }, file_name)

    @staticmethod
    def gather_subject_educator_data(entry: SubjectEducator) -> Tuple[Dict[str, Any], str]:
        """Gather data for SubjectEducator entity."""
        file_name = f"SubjectEducator_{entry.educator_id}_{entry.subject_id}_{entry.academic_session}_{entry.term}"

        return ({
            "subject_educator": {
                "id": str(entry.id),
                "subject_id": str(entry.subject_id),
                "educator_id": str(entry.educator_id),
                "level_id": str(entry.level_id),
                "academic_year": entry.academic_session,
                "term": entry.term,
                "is_active": entry.is_active,
                "date_assigned": entry.date_assigned,
                "created_at": entry.created_at,
                "created_by": str(entry.created_by) if entry.created_by else None,
                "last_modified_at": entry.last_modified_at,
                "last_modified_by": str(entry.last_modified_by) if entry.last_modified_by else None,
                "archived_at": entry.archived_at,
                "archived_by": str(entry.archived_by) if entry.archived_by else None,
                "archive_reason": entry.archive_reason,
            },
            "educator": {
                "id": str(entry.teacher.id),
                "name": f"{entry.teacher.first_name} {entry.teacher.last_name}",
                "email": entry.teacher.email_address,
            } if entry.teacher else None,
            "subject": {
                "id": str(entry.subject.id),
                "name": entry.subject.name
            } if entry.subject else None
        }, file_name)


