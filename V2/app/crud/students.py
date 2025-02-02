from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from ..schemas.profiles import NewStudent, UpdateStudent, Student
from ..database.models.profiles import Students
from sqlalchemy.orm import Session
from ..services.profiles import profile_service


class StudentCrud:
    def __init__(self, db:Session):
        self.profile_service = profile_service
        self.db = db


    def get_all_students(self) -> list[Student]:
        students = self.db.query(Students).order_by(Students.first_name).all()
        return [Student.model_validate(student) for student in students]

    def get_student(self, studentId: str) -> dict:
        student = (
            self.db.query(Students)
            .filter(func.lower(Students.student_id) == studentId.strip().lower())
            .first()
        )
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
        # student_model = Student.model_validate(student)
        # return student_model.model_dump(exclude={"is_active", "last_login", "is_soft_deleted",
        #                                    "deleted_at", "deleted_by", "deletion_reason",
        #                                    "deletion_eligible"})


    def create_student(self, new_student:NewStudent):
        data = new_student.model_dump()
        data['id'] = uuid4()
        try:
            student_id = data['student_id']
            student_id  = self.profile_service.validate_student_id(student_id)
        except Exception:
            raise HTTPException(status_code=400)
        except Exception:
            raise HTTPException(status_code=400)
        
        new_student = Students(**data)
        try:
            self.db.add(new_student)
            self.db.commit()
            return Student.model_validate(new_student)
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=409, detail=f"Student ID {new_student.student_id} already exists")


    def update_student(self):
        pass


    def soft_delete_student(self):
            pass

    def delete_student(self):
       pass

