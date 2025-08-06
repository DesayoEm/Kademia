from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer


from app.core.identity.factories.student import StudentFactory
from app.core.identity.models.student import Student
from app.core.shared.exceptions.academic_structure_errors import ClassLevelMismatchError
from app.core.shared.services.audit_export_service.export import ExportService
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService


class StudentService:
    def __init__(self, session: Session, current_user = None):
        self.session = session
        self.current_user = current_user
        self.export_service = ExportService(session)
        self.factory = StudentFactory(session = self.session, current_user=self.current_user)
        self.archive_service = ArchiveService(session, current_user=current_user)


    def generate_student_id(self, start_year: int):
        """
        Generate a unique student ID.
        Args:
            start_year: Academic year start year
        """
        school_code = 'SCH'
        year_code = str(start_year)[2:]
        prefix = f"{school_code}-{year_code}-"
        pattern = f"{prefix}%"

        result = self.session.query(
            func.max(
                func.cast(
                    func.substring(Student.student_id, len(prefix) + 1),Integer
                )
            )
        ).filter(
            Student.student_id.like(pattern),
            Student.session_start_year == start_year
        ).scalar()

        next_serial = 1 if result is None else result + 1
        formatted_serial = f"{next_serial:05d}"
        student_id = f"{school_code}-{year_code}-{formatted_serial}"
        return student_id


    def assign_department(self, stu_id: UUID, department_id: UUID | None = None):
        """Assign a student's department"""
        if not department_id:
            return self.factory.update_student(stu_id, {"department_id": None})

        return self.factory.update_student(stu_id, {"department_id": department_id})


    def assign_class(self, stu_id: UUID, class_id: UUID | None = None):
        """Assign a student's class"""
        if not class_id:
            return self.factory.update_student(stu_id, {"class_id": None})

        from app.core.academic_structure.factories.classes import ClassFactory
        class_factory = ClassFactory(session=self.session, current_user=self.current_user)

        class_ = class_factory.get_class(class_id)
        student = self.factory.get_student(stu_id)

        if student.level_id != class_.level_id:
            raise ClassLevelMismatchError(stu_id, class_id)

        return self.factory.update_student(stu_id, {"class_id": class_id})


    def change_guardian(self, stu_id: UUID, guardian_id: UUID):
        """Change a student's guardian"""
        return self.factory.update_student(stu_id, {"guardian_id": guardian_id})

    def cascade_student_archive(self, student_id: UUID, reason: str):
        student = self.factory.get_student(student_id)
        self.archive_service.cascade_archive_object(Student, student, reason)


    def export_student_audit(self, stu_id: UUID, export_format: str) -> str:
        """Export Student object and its associated data
        Args:
            stu_id: Student UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Student, stu_id, export_format
        )

