from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.curriculum.crud.student_subject import StudentSubjectCrud
from V2.app.core.curriculum.schemas.student_subject import (
   StudentSubjectResponse, StudentSubjectFilterParams
)

router = APIRouter()

@router.get("/", response_model=List[StudentSubjectResponse])
def get_archived_student_subjects(filters: StudentSubjectFilterParams = Depends(),db: Session = Depends(get_db)):
    student_subject_crud = StudentSubjectCrud(db)
    return student_subject_crud.get_all_archived_student_subjects(filters)


@router.get("/{student_subject_id}", response_model=StudentSubjectResponse)
def get_archived_student_subject(student_subject_id: UUID, db: Session = Depends(get_db)):
    student_subject_crud = StudentSubjectCrud(db)
    return student_subject_crud.get_archived_student_subject(student_subject_id)


@router.patch("/{student_subject_id}", response_model=StudentSubjectResponse)
def restore_student_subject(student_subject_id: UUID,db: Session = Depends(get_db)):
    student_subject_crud = StudentSubjectCrud(db)
    return student_subject_crud.restore_student_subject(student_subject_id)


@router.delete("/{student_subject_id}", status_code=204)
def delete_archived_student_subject(student_subject_id: UUID, db: Session = Depends(get_db)):
    student_subject_crud = StudentSubjectCrud(db)
    return student_subject_crud.delete_archived_student_subject(student_subject_id)




