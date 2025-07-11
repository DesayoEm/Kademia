from typing import Dict, Tuple, Any
from V2.app.core.identity.models.student import Student



class StudentGatherer:
    """Gatherer for student-related entities"""

    @staticmethod
    def gather_student_data(student: Student) -> Tuple[Dict[str, Any], str]:
        """Gather data for Student entity."""
        file_name = f"Student_{student.first_name}_{student.last_name}"

        subjects_taken = student.subjects_taken
        grades = student.grades
        total_grades = student.total_grades
        classes_repeated = student.classes_repeated
        department_transfers = student.department_transfers
        class_transfers = student.class_transfers
        documents = student.documents_owned
        awards = student.awards_earned

        return ({
                    "student": {
                        "id": str(student.id),
                        "student_id": student.student_id,
                        "full_name": f"{student.first_name} {student.last_name}",
                        "gender": student.gender,
                        "status": student.status,
                        "date_of_birth": str(student.date_of_birth),
                        "image_url": student.image_url,
                        "access_level": student.access_level,
                        "user_type": student.user_type,
                        "level": {
                            "id": str(student.level_id) if student.level_id else None,
                            "name": student.level.name if student.level else None
                        },
                        "class": {
                            "id": str(student.class_id) if student.class_id else None,
                            "level": student.class_.academic_level.name if student.class_ and student.class_.academic_level else None,
                            "code": student.class_.code.value if student.class_ else None
                        },
                        "department": {
                            "id": str(student.department_id) if student.department_id else None,
                            "name": student.department.name if student.department else None,
                            "code": student.department.code if student.department else None
                        },
                        "is_repeating": student.is_repeating,
                        "session_start_year": student.session_start_year,
                        "date_left": str(student.date_left) if student.date_left else None,
                        "graduation_date": str(student.graduation_date) if student.graduation_date else None,
                        "created_at": student.created_at,
                        "created_by": student.created_by_staff,
                        "last_modified_at": student.last_modified_at,
                        "last_modified_by": student.last_modified_by_staff,
                    },
                    "guardian": {
                        "id": str(student.guardian_id),
                        "full_name": f"{student.guardian.first_name} {student.guardian.last_name}" if student.guardian else None,
                        "phone": student.guardian.phone if student.guardian else None,
                        "email_address": student.guardian.email_address if student.guardian else None
                    },
                    "subjects_taken": [
                        {
                            "id": str(subject.id),
                            "subject_name": subject.subject.name if subject.subject else None,
                            "academic_year": subject.academic_year,
                            "term": subject.term,
                            "is_active": subject.is_active
                        }
                        for subject in subjects_taken
                    ],
                    "grades": [
                        {
                            "id": str(grade.id),
                            "subject": grade.subject.name if grade.subject else None,
                            "academic_year": grade.academic_year,
                            "term": grade.term,
                            "type": grade.type,
                            "score": grade.score,
                            "feedback": grade.feedback,
                            "graded_by": grade.grader.first_name + " " + grade.grader.last_name if grade.grader else None
                        }
                        for grade in grades
                    ],
                    "total_grades": [
                        {
                            "id": str(grade.id),
                            "subject": grade.subject.name if grade.subject else None,
                            "academic_year": grade.academic_year,
                            "term": grade.term,
                            "total_score": grade.total_score,
                            "rank": grade.rank
                        }
                        for grade in total_grades
                    ],
                    "academic_history": {
                        "classes_repeated": [
                            {
                                "id": str(repetition.id),
                                "academic_year": repetition.academic_year,
                                "previous_level": repetition.previous_level.name if repetition.previous_level else None,
                                "new_level": repetition.new_level.name if repetition.new_level else None,
                                "previous_class": f"{repetition.previous_class.academic_level.name} {repetition.previous_class.code}" if repetition.previous_class and repetition.previous_class.academic_level else None,
                                "new_class": f"{repetition.new_class.academic_level.name} {repetition.new_class.code}" if repetition.new_class and repetition.new_class.academic_level else None,
                                "reason": repetition.reason,
                                "status": repetition.status,
                                "updated_by": repetition.status_updated_staff.first_name + " " + repetition.status_updated_staff.last_name if repetition.status_updated_staff else None,
                                "updated_at": str(
                                    repetition.status_updated_at) if repetition.status_updated_at else None,
                                "rejection_reason": repetition.rejection_reason
                            }
                            for repetition in classes_repeated
                        ],
                        "department_transfers": [
                            {
                                "id": str(transfer.id),
                                "academic_year": transfer.academic_year,
                                "previous_department": transfer.former_dept.name if transfer.former_dept else None,
                                "new_department": transfer.new_dept.name if transfer.new_dept else None,
                                "previous_level": transfer.previous_level_rel.name if transfer.previous_level_rel else None,
                                "new_level": transfer.new_level_rel.name if transfer.new_level_rel else None,
                                "previous_class": f"{transfer.former_class_rel.academic_level.name} {transfer.former_class_rel.code}" if transfer.former_class_rel and transfer.former_class_rel.academic_level else None,
                                "new_class": f"{transfer.new_class_rel.academic_level.name} {transfer.new_class_rel.code}" if transfer.new_class_rel and transfer.new_class_rel.academic_level else None,
                                "reason": transfer.reason,
                                "status": transfer.status,
                                "updated_by": transfer.status_changer.first_name + " " + transfer.status_changer.last_name if transfer.status_changer else None,
                                "updated_at": str(transfer.status_updated_at) if transfer.status_updated_at else None,
                                "rejection_reason": transfer.rejection_reason
                            }
                            for transfer in department_transfers
                        ],
                        "class_transfers": [
                            {
                                "id": str(transfer.id),
                                "academic_year": transfer.academic_year,
                                "previous_class": f"{transfer.previous_class.academic_level.name} {transfer.previous_class.code}" if transfer.previous_class and transfer.previous_class.academic_level else None,
                                "new_class": f"{transfer.new_class.academic_level.name} {transfer.new_class.code}" if transfer.new_class and transfer.new_class.academic_level else None,
                                "reason": transfer.reason,
                                "status": transfer.status,
                                "updated_by": transfer.status_changer.first_name + " " + transfer.status_changer.last_name if transfer.status_changer else None,
                                "updated_at": str(transfer.status_updated_at) if transfer.status_updated_at else None,
                                "rejection_reason": transfer.rejection_reason
                            }
                            for transfer in class_transfers
                        ]
                    },
                    "documents": [
                        {
                            "id": str(document.id),
                            "title": document.title,
                            "academic_year": document.academic_year,
                            "document_type": document.document_type,
                            "file_url": document.file_url
                        }
                        for document in documents
                    ],
                    "awards": [
                        {
                            "id": str(award.id),
                            "title": award.title,
                            "description": award.description,
                            "academic_year": award.academic_year,
                            "file_url": award.file_url
                        }
                        for award in awards
                    ]
                }, file_name)


