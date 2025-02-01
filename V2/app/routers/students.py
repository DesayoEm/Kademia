from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ..database.utils import get_db
from ..crud.students import StudentCrud


router = APIRouter()

@router.get("/students/")
def read_students(db: Session = Depends(get_db)):
    pass

@router.get("/students/{student_id}")
def read_student(student_id: str, db: Session = Depends(get_db)):
    pass

@router.post("/students/{student_id}")
def create_student(db: Session = Depends(get_db)):
    pass

@router.put("/students/{student_id}")
def update_student(student_id: str, db: Session = Depends(get_db)):
    pass

@router.delete("/students/{student_id}")
def delete_student(student_id: str, db: Session = Depends(get_db)):
    pass


