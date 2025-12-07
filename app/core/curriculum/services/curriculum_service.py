from sqlalchemy.orm import Session, joinedload
from datetime import date
from uuid import UUID
from app.core.curriculum.models.curriculum import (
    Subject,
    AcademicLevelSubject,
    StudentSubject,
    SubjectEducator,
)
from app.core.identity.factories.student import StudentFactory
from app.core.identity.models.student import Student
from app.core.shared.exceptions.curriculum_errors import AcademicLevelMismatchError

from app.core.shared.schemas.enums import Semester
from app.core.shared.services.pdf_service.templates.course_list import CourseListPDF


class CurriculumService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user
        self.student_factory = StudentFactory(session, Student, current_user)
        self.pdf_service = CourseListPDF()

    def check_academic_level(
        self, student_id: UUID, level_id: UUID, academic_level_subject_id: UUID
    ):
        student = self.student_factory.get_student(student_id)
        if student.level_id != level_id:
            raise AcademicLevelMismatchError(student_id, level_id)

        return academic_level_subject_id

    def generate_enrollment_list(
        self, student_id: UUID, academic_session: str, semester: Semester
    ):
        student = self.student_factory.get_student(student_id)
        student_name = f"{student.first_name} {student.last_name}"
        today = date.today()
        date_generated = f"{today.day} {today.strftime('%B')} {today.year}"

        enrollments = (
            self.session.query(StudentSubject)
            .options(
                joinedload(StudentSubject.subject).joinedload(
                    AcademicLevelSubject.subject
                ),
                joinedload(StudentSubject.subject)
                .joinedload(AcademicLevelSubject.educators)
                .joinedload(SubjectEducator.teacher),
            )
            .filter(
                StudentSubject.student_id == student_id,
                StudentSubject.academic_session == academic_session,
                StudentSubject.semester == semester,
            )
            .all()
        )

        enrollment_list = []
        for enrollment in enrollments:
            course_code = enrollment.subject.code
            course_title = enrollment.subject.subject.name

            active_educators = [
                edu for edu in enrollment.subject.educators if edu.is_active
            ]
            if active_educators:
                educator_name = f"{active_educators[0].teacher.first_name} {active_educators[0].teacher.last_name}"
            else:
                educator_name = "No Teacher Assigned"

            enrollment_list.append(
                {
                    "course_code": course_code,
                    "course_title": course_title,
                    "educator_name": educator_name,
                }
            )

        return {
            "student_name": student_name,
            "semester": semester.value,
            "academic_session": academic_session,
            "date_generated": date_generated,
            "enrollment_list": enrollment_list,
        }

    def render_enrollment_list_pdf(
        self, student_id: UUID, academic_session: str, semester: Semester
    ):
        student = self.student_factory.get_student(student_id)
        student_name = f"{student.first_name} {student.last_name}"
        file_name = f"{student_name} {academic_session} course list"

        data = self.generate_enrollment_list(student_id, academic_session, semester)

        return self.pdf_service.render_pdf(data, file_name)
