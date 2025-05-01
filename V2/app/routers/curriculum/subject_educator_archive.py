from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.curriculum.crud.subject_educator import SubjectEducatorCrud
from V2.app.core.curriculum.schemas.subject_educator import (
   SubjectEducatorResponse, SubjectEducatorFilterParams
)

router = APIRouter()

@router.get("/", response_model=List[SubjectEducatorResponse])
def get_archived_subject_educators(filters: SubjectEducatorFilterParams = Depends(),db: Session = Depends(get_db)):
    subject_educator_crud = SubjectEducatorCrud(db)
    return subject_educator_crud.get_all_archived_subject_educators(filters)


@router.get("/{subject_educator_id}", response_model=SubjectEducatorResponse)
def get_archived_subject_educator(subject_educator_id: UUID, db: Session = Depends(get_db)):
    subject_educator_crud = SubjectEducatorCrud(db)
    return subject_educator_crud.get_archived_subject_educator(subject_educator_id)


@router.patch("/{subject_educator_id}", response_model=SubjectEducatorResponse)
def restore_subject_educator(subject_educator_id: UUID,db: Session = Depends(get_db)):
    subject_educator_crud = SubjectEducatorCrud(db)
    return subject_educator_crud.restore_subject_educator(subject_educator_id)


@router.delete("/{subject_educator_id}", status_code=204)
def delete_archived_subject_educator(subject_educator_id: UUID, db: Session = Depends(get_db)):
    subject_educator_crud = SubjectEducatorCrud(db)
    return subject_educator_crud.delete_archived_subject_educator(subject_educator_id)




