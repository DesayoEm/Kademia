from sqlalchemy.orm import Session
from sqlalchemy import func, Integer
from V2.app.core.shared.database.models import Student

class StudentService:
    def __init__(self, session: Session):
        self.session = session

    def generate_student_id(self, start_year: int):
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