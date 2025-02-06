from ..database.models.data_enums import ArchiveReason
from ..schemas.profiles import NewStudent, UpdateStudent, Student
from ..database.models.profiles import Students
from sqlalchemy.orm import Session
from ..services.students import StudentService, ArchivedStudentService
from ..services.base import CrudService


class StudentCrud(CrudService):
    def __init__(self, db:Session):
        super().__init__(db, Students)
        self.student_service = StudentService(db)
        self.archive_service = ArchivedStudentService(db)

    def create_student(self, new_student:NewStudent):
        return self.student_service.create_student(new_student)


    def read_all_students(self) -> list[Student]:
        return self.student_service.get_all_students()


    def read_student(self, student_id: str) -> dict:
        return self.student_service.get_student(student_id)


    def update_student(self, student_id:str, data:UpdateStudent):
        return self.student_service.update_student(student_id, data)


    def archive_student(self, student_id:str, reason: ArchiveReason):
        return self.student_service.archive_student(student_id, reason)


    def delete_student(self, student_id:str):
        return self.student_service.delete_student(student_id)


    def read_archived_students(self, student_id: str) -> dict:
        return self.archive_service.get_archived_students()


    def read_archived_student(self, student_id: str) -> dict:
        return self.archive_service.get_archived_student(student_id)


    def restore_student(self, student_id):
        return self.archive_service.restore_student(student_id)


    def delete_archived_student(self, student_id:str):
        return self.archive_service.delete_archived_student(student_id)
