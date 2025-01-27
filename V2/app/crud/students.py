from fastapi import HTTPException
from ..schemas.profiles import NewStudent
from ..database.models.profiles import Students
from ..services.students import student_service
from sqlalchemy.orm import Session


class StudentCrud:
    def __init__(self, db:Session):
        self.student_service = student_service
        self.session = db

    def get_all_students(self):
        students = self.session.query(Students).all()
        return students

    def get_student(self, student_id:str):
        student = self.session.query(Students).filter_by(student_id = student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student.model_dump()

    def create_student(self, new_student:NewStudent):
        pass

    def update_student(self):
        pass

    def delete_student(self):
        pass