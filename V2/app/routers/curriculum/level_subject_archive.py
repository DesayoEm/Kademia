from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.curriculum.crud.academic_level_subject import AcademicLevelSubjectCrud
from V2.app.core.curriculum.schemas.academic_level_subject import (
   AcademicLevelSubjectResponse, AcademicLevelSubjectFilterParams
)

router = APIRouter()

@router.get("/", response_model=List[AcademicLevelSubjectResponse])
def get_archived_level_subjects(filters: AcademicLevelSubjectFilterParams = Depends(),db: Session = Depends(get_db)):
    level_subject_crud = AcademicLevelSubjectCrud(db)
    return level_subject_crud.get_all_archived_level_subjects(filters)


@router.get("/{level_subject_id}", response_model=AcademicLevelSubjectResponse)
def get_archived_level_subject(level_subject_id: UUID, db: Session = Depends(get_db)):
    level_subject_crud = AcademicLevelSubjectCrud(db)
    return level_subject_crud.get_archived_level_subject(level_subject_id)


@router.patch("/{level_subject_id}", response_model=AcademicLevelSubjectResponse)
def restore_level_subject(level_subject_id: UUID,db: Session = Depends(get_db)):
    level_subject_crud = AcademicLevelSubjectCrud(db)
    return level_subject_crud.restore_level_subject(level_subject_id)


@router.delete("/{level_subject_id}", status_code=204)
def delete_archived_level_subject(level_subject_id: UUID, db: Session = Depends(get_db)):
    level_subject_crud = AcademicLevelSubjectCrud(db)
    return level_subject_crud.delete_archived_level_subject(level_subject_id)




