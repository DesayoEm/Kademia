from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from ..schemas.profiles import NewStudent, UpdateStudent, Student
from ..database.models.profiles import Students
from sqlalchemy.orm import Session
from ..services.profile_validation import profile_validator
from ..exceptions.profiles import StudentIdFormatError, IdYearError, DuplicateStudentIDError, StudentNotFoundError
from ..crud.base import BaseCrud


class StudentService(BaseCrud):
    def __init__(self, db:Session):
        super().__init__(db, Students)
        self.profile_validator = profile_validator


    def get_all_students(self) -> list[Student]:
        students = self.base_query().order_by(Students.first_name).all()
        return [Student.model_validate(student) for student in students]


    def get_student(self, student_id: str) -> dict:
        student = (
            self.base_query()
            .filter(func.lower(Students.student_id) == student_id.strip().lower())
            .first()
        )
        if not student:
            raise StudentNotFoundError
        return student
        # student_model = Student.model_validate(student)
        # return student_model.model_dump(exclude={"is_active", "last_login", "is_soft_deleted",
        #                                    "deleted_at", "deleted_by", "deletion_reason",
        #                                    "deletion_eligible"})




    def create_student(self, new_student:NewStudent):
        data = new_student.model_dump()
        data['id'] = uuid4()
        try:
            student_id = data['student_id'].strip()
            student_id  = self.profile_service.validate_student_id(student_id)
        except StudentIdFormatError as e:
            raise HTTPException(status_code=400, detail = str(e))
        except IdYearError as e:
            raise HTTPException(status_code=400, detail= str(e))

        new_student = Students(**data)
        try:
            self.db.add(new_student)
            self.db.commit()
            return Student.model_validate(new_student)
        except IntegrityError:
            self.db.rollback()
            raise DuplicateStudentIDError


    def update_student(self, student_id:str, data:UpdateStudent):
        student= self.get_student(student_id)
        try:
            for key,value in data.model_dump(exclude_unset=True).items():
                setattr(student, key, value)
            self.db.commit()
            self.db.refresh(student)
            return student
        except IntegrityError:
            self.db.rollback()
            raise DuplicateStudentIDError


    def archive_student(self, student_id:str):
        student= self.get_student(student_id)
        student.is_archived = True
        # student.archived_by = archived_by
        # student.archived_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(student)
        return student


    def delete_student(self, student_id:str):
        student= self.get_student(student_id)
        self.db.delete(student)
        self.db.commit()

