from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.curriculum.crud.subject import SubjectCrud
from V2.app.core.curriculum.schemas.subject import SubjectFilterParams, SubjectResponse



router = APIRouter()


@router.get("/", response_model=list[SubjectResponse])
def get_archived_levels(filters: SubjectFilterParams = Depends(),db: Session = Depends(get_db)):
    subject_crud = SubjectCrud(db)
    return subject_crud.get_all_archived_subjects(filters)


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_archived_level(subject_id: UUID, db: Session = Depends(get_db)):
    subject_crud = SubjectCrud(db)
    return subject_crud.get_archived_subject(subject_id)


@router.patch("/{subject_id}", response_model=SubjectResponse)
def restore_level(subject_id: UUID,db: Session = Depends(get_db)):
    subject_crud = SubjectCrud(db)
    return subject_crud.restore_subject(subject_id)


@router.delete("/{subject_id}", status_code=204)
def delete_archived_level(subject_id: UUID, db: Session = Depends(get_db)):
    subject_crud = SubjectCrud(db)
    return subject_crud.delete_archived_subject(subject_id)




