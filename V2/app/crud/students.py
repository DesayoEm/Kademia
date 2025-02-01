from fastapi import HTTPException
from ..schemas.profiles import NewStudent, UpdateStudent
from ..database.models.profiles import Students
from sqlalchemy.orm import Session
from ..services.students import student_service


class StudentCrud:
    def __init__(self, db:Session):
        self.student_service = student_service
        self.db = db

    def get_all_students(self, session:Session):
        pass

    def get_student(self, student_id:str, session:Session):
        pass

    def create_student(self, new_student:NewStudent, session:Session):
       pass

    def update_student(self):
        pass

    def delete_student(self):
        pass