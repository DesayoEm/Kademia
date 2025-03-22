from sqlalchemy.orm import Session
from ....database.models.users import Student
from ....database.models.student_organization import StudentDepartment

class StudentService:
    def __init__(self, session: Session):
        self.session = session

    def generate_department_code(self, department_id):
        department = self.session.query(StudentDepartment).filter(
            StudentDepartment.id == department_id).first()

        if department.name.lower() == "science":
            return "SCI"
        if department.name.lower() == "science":
            return "SCI"
        if department.name.lower() == "science":
            return "SCI"

    def generate_student_id(self, department: str, start_year: int):
        last_student = self.session.query(Student).filter(
            Student.department_id == department and Student.session_start_year == start_year
                        ).first()
        #slice the str
        #convert to int
        #find the max

        student_id = "Nonsense id"
        return student_id