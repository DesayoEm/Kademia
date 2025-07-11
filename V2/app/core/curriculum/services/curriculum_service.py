from sqlalchemy.orm import Session, joinedload
from datetime import date
from uuid import UUID

from V2.app.core.shared.services.pdf_service.reportlab_base import ReportLabService
from V2.app.core.curriculum.models.curriculum import Subject, AcademicLevelSubject, StudentSubject, SubjectEducator
from V2.app.core.identity.factories.student import StudentFactory
from V2.app.core.identity.models.student import Student
from V2.app.core.shared.exceptions.curriculum_errors import AcademicLevelMismatchError
from V2.app.core.shared.services.audit_export_service.export import ExportService
from V2.app.core.shared.schemas.enums import Term
from V2.app.core.shared.services.pdf_service.templates.course_list import CourseListPDF
from V2.app.infra.settings import config

class CurriculumService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user
        self.export_service = ExportService(self.session)
        self.student_factory = StudentFactory(session, Student, current_user)
        self.pdf_service = CourseListPDF()
        self.export_dir = config.EXPORT_DIR


    def check_academic_level(self, student_id: UUID, level_id:UUID, academic_level_subject_id:UUID):
        student = self.student_factory.get_student(student_id)
        if student.level_id != level_id:
            raise AcademicLevelMismatchError(student_id, level_id)

        return academic_level_subject_id


    def generate_student_course_list(self, student_id: UUID, academic_session: str, term: Term):
        student = self.student_factory.get_student(student_id)
        student_name = f"{student.first_name} {student.last_name}"
        today = date.today()
        date_generated = f"{today.day} {today.strftime('%B')} {today.year}"

        enrollments = self.session.query(StudentSubject).options(
            joinedload(StudentSubject.subject)
            .joinedload(AcademicLevelSubject.subject),joinedload(StudentSubject.subject)
            .joinedload(AcademicLevelSubject.educators)
            .joinedload(SubjectEducator.teacher)
        ).filter(
            StudentSubject.student_id == student_id,
            StudentSubject.academic_session == academic_session,
            StudentSubject.term == term
        ).all()

        enrollment_list = []
        for enrollment in enrollments:
            course_code = enrollment.subject.code
            course_title = enrollment.subject.subject.name

            active_educators = [edu for edu in enrollment.subject.educators if edu.is_active]
            if active_educators:
                educator_name = f"{active_educators[0].teacher.first_name} {active_educators[0].teacher.last_name}"
            else:
                educator_name = "No Teacher Assigned"

            enrollment_list.append({
                "course_code": course_code,
                "course_title": course_title,
                "educator_name": educator_name
            })

        return {
            "student_name": student_name,
            "term": term.value,
            "academic_session": academic_session,
            "date_generated": date_generated,
            "enrollment_list": enrollment_list
        }


    def render_course_list_pdf(self, student_id: UUID, academic_session: str, term: Term):
        student = self.student_factory.get_student(student_id)
        student_name = f"{student.first_name} {student.last_name}"
        file_name = f"{student_name} {academic_session} course list"

        data = self.generate_student_course_list(student_id, academic_session, term)

        return self.pdf_service.render_pdf(data, file_name)


    def export_subject_audit(self, subject_id: UUID, export_format: str) -> str:
        """Export subject and its associated data
        Args:
            subject_id: subject UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Subject, subject_id, export_format
        )


    def export_level_subject_audit(self, level_subject_id: UUID, export_format: str) -> str:
        """Export level subject and its associated data
        Args:
            level_subject_id: subject UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Subject, level_subject_id, export_format
        )


