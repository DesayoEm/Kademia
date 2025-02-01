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

@router.get("/students/{student_id}", response_model=Student)
def read_student(student_id: str, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.get_student(student_id)

@router.post("/students/{student_id}")
def create_student(db: Session = Depends(get_db)):
    pass

@router.put("/students/{student_id}")
def update_student(student_id: str, db: Session = Depends(get_db)):
    pass

@router.delete("/students/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    pass


