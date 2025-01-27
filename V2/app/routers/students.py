from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ..database.utils import get_db
from ..crud.students import StudentCrud

#uvicorn app.main:app --port 2000 --reload
router = APIRouter()

@router.get("/students/{student_id}")
def read_student(student_id: str, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db=db)
    return student_crud.get_student(student_id)

