from sqlalchemy.orm import Session
from ..schemas.profiles import NewStudent, UpdateStudent, Student
from fastapi import Depends, APIRouter
from ..database.utils import get_db
from ..crud.students import StudentCrud


router = APIRouter()


@router.get("/students/", response_model = list[Student])
def read_students(db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.get_all_students()


@router.get("/students/{student_id}")
def read_student(studentId: str, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.get_student(studentId)

@router.post("/students/", status_code = 201)
def create_student(new_student:NewStudent, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.create_student(new_student)


@router.put("/students/{student_id}")
def update_student(student_id: str, data:UpdateStudent, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.update_student(student_id, data)


@router.patch("/students/{student_id}")
def archive_student(student_id: str, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.archive_student(student_id)


@router.delete("/students/{student_id}", status_code = 204)
def delete_student(student_id: str, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.delete_student(student_id)

