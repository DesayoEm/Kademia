from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer
from V2.app.core.identity.models.student import Student
from V2.app.core.shared.services.export_service.export import ExportService


class StudentService:
    def __init__(self, session: Session, current_user = None):
        self.session = session
        self.current_user = current_user
        self.export_service = ExportService(session)


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


    def export_student(self, stu_id: UUID, export_format: str) -> str:
        """Export Student object and its associated data
        Args:
            stu_id: Student UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Student, stu_id, export_format
        )