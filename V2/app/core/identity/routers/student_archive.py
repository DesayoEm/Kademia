from sqlalchemy.orm import Session
from uuid import UUID
from V2.app.core.identity.schemas.student import StudentResponse, StudentFilterParams
from fastapi import Depends, APIRouter
from V2.app.core.shared.database.session_manager import get_db
from V2.app.core.identity.crud.student import StudentCrud
from fastapi import Query
from typing import Annotated

router = APIRouter()

@router.get("/", response_model=list[StudentResponse])
def get_archived_students(filters: Annotated[StudentFilterParams, Query()],
        db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.get_all_archived_student(filters)


@router.get("/{student_id}", response_model=StudentResponse)
def get_archived_student(student_id: UUID, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.get_archived_student(student_id)


@router.patch("/{student_id}", response_model=StudentResponse)
def restore_student(student_id: UUID, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.restore_student(student_id)


@router.delete("/{student_id}", status_code=204)
def delete_archived_student(student_id: UUID, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.delete_archived_student(student_id)











