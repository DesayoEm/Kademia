from sqlalchemy.orm import Session
from uuid import UUID
from ....schemas.users.student import StudentCreate, StudentUpdate, StudentResponse, StudentFilterParams
from fastapi import Depends, APIRouter
from ....database.session_manager import get_db
from ....crud.users.student import StudentCrud
from ....schemas.shared_models import ArchiveRequest
from fastapi import Query
from typing import Annotated

router = APIRouter()


@router.post("/", response_model= StudentResponse, status_code=201)
def create_student(data:StudentCreate,
                db: Session = Depends(get_db)):
        student_crud = StudentCrud(db)
        return student_crud.create_student(data)


@router.get("/", response_model=list[StudentResponse])
def get_students(filters: Annotated[StudentFilterParams, Query()],
                db: Session = Depends(get_db)):
        student_crud = StudentCrud(db)
        return student_crud.get_all_students(filters)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: UUID, db: Session = Depends(get_db)):
        student_crud = StudentCrud(db)
        return student_crud.get_student(student_id)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(data: StudentUpdate, student_id: UUID,
                         db: Session = Depends(get_db)):
        student_crud = StudentCrud(db)
        return student_crud.update_student(student_id, data)


@router.patch("/{student_id}", status_code=204)
def archive_student(student_id: UUID, reason:ArchiveRequest,
                          db: Session = Depends(get_db)):
        student_crud = StudentCrud(db)
        return student_crud.archive_student(student_id, reason.reason)


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: UUID, db: Session = Depends(get_db)):
        student_crud = StudentCrud(db)
        return student_crud.delete_student(student_id)











