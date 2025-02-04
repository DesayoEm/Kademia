from sqlalchemy.orm import Session
from ..schemas.profiles import NewStudent, UpdateStudent, Student
from fastapi import Depends, APIRouter
from ..database.utils import get_db
from ..crud.students import StudentCrud
from fastapi import HTTPException
from ..exceptions.profiles import StudentIdFormatError, IdYearError, DuplicateStudentIDError, StudentNotFoundError


router = APIRouter()


@router.get("/students/", response_model = list[Student])
def read_students(db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.get_all_students()


@router.get("/students/{student_id}")
def get_student(stu_id: str, db: Session = Depends(get_db)):
    try:
        student_crud = StudentCrud(db)
        return student_crud.get_student(stu_id)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/students/", status_code = 201)
def create_student(new_student:NewStudent, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.create_student(new_student)


@router.put("/students/{student_id}")
def update_student(stu_id: str, data:UpdateStudent, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.update_student(stu_id, data)


@router.patch("/students/{student_id}")
def archive_student(stu_id: str, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.archive_student(stu_id)


@router.delete("/students/{student_id}", status_code = 204)
def delete_student(student_id: str, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.delete_student(student_id)

