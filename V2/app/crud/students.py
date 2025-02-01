from fastapi import HTTPException
from typing import List
from ..schemas.profiles import NewStudent, UpdateStudent, Student
from ..database.models.profiles import Students
from sqlalchemy.orm import Session
from ..services.students import student_service


class StudentCrud:
    def __init__(self, db:Session):
        self.student_service = student_service
        self.db = db

    def get_all_students(self) -> List[Students]:
        students = self.db.query(Students).order_by(Students.first_name).all()
        return [Student.model_validate(student) for student in students]

    def get_student(self, student_id:str, session:Session):
        pass

    def create_student(self, new_student:NewStudent, session:Session):
       pass

    def update_student(self):
        pass

    def delete_student(self):
       pass

student_crud = StudentCrud()