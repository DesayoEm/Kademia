from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from uuid import uuid4

from .exceptions.profiles import NoArchiveRecords
from ..database.models.data_enums import ArchiveReason
from ..schemas.profiles import NewStudent, UpdateStudent, Student
from ..database.models.profiles import Students
from sqlalchemy.orm import Session
from ..services.profile_validation import profile_validator
from ..services.exceptions.profiles import DuplicateStudentIDError, StudentNotFoundError, ArchivedStudentNotFound
from ..services.base import CrudService
SYSTEM_USER_ID="00000000-0000-0000-0000-000000000000"


class StudentService(CrudService):
    def __init__(self, db:Session):
        super().__init__(db, Students)
        self.profile_validator = profile_validator

    def create_student(self, new_student:NewStudent):
        data = new_student.model_dump()
        data['id'] = uuid4()
        student_id = data['student_id'].strip()
        student_id  = self.profile_validator.validate_student_id(student_id)

        new_student = Students(**data)
        try:
            self.db.add(new_student)
            self.db.commit()
            return Student.model_validate(new_student)
        except IntegrityError:
            self.db.rollback()
            raise DuplicateStudentIDError(student_id)


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
            raise DuplicateStudentIDError(data['student_id'])


    def archive_student(self, student_id:str, reason: ArchiveReason):
        student= self.get_student(student_id)
        #archive all related records first
        for doc in student.documents_owned:
            doc.archive(SYSTEM_USER_ID, reason)

        for grade in student.grades:
            grade.archive(SYSTEM_USER_ID, reason)

        for total_grade in student.total_grades:
            total_grade.archive(SYSTEM_USER_ID, reason)

        for transfer in student.transfers:
            transfer.archive(SYSTEM_USER_ID, reason)

        for repetition in student.classes_repeated:
            repetition.archive(SYSTEM_USER_ID, reason)

        student.archive(SYSTEM_USER_ID, reason)

        self.db.commit()
        self.db.refresh(student)
        return student

    def delete_student(self, student_id:str):
        student= self.get_student(student_id)
        self.db.delete(student)
        self.db.commit()


class ArchivedStudentService():
    def __init__(self, db:Session):
        self.db = db

    def get_archived_students(self):
        students = self.db.query(Students).filter(Students.is_archived == True).all()
        if not students:
            raise NoArchiveRecords
        return students


    def get_archived_student(self, student_id):
        student =  (self.db.query(Students)
                    .filter(Students.is_archived == True)
                    .filter(Students.student_id == student_id)
                    .first())
        if not student:
            raise ArchivedStudentNotFound
        return student


    def restore_student(self, student_id:str):
        student= self.get_archived_student(student_id)

        for doc in student.documents_owned:
            doc.restore()

        for grade in student.grades:
            grade.restore()

        for total_grade in student.total_grades:
            total_grade.restore()

        for transfer in student.transfers:
            transfer.restore()

        for repetition in student.classes_repeated:
            repetition.restore()

        student.restore()

        self.db.commit()
        self.db.refresh(student)
        return student

    def delete_archived_student(self, student_id):
        student =  self.get_archived_student(student_id)
        self.db.delete(student)
        self.db.commit()



