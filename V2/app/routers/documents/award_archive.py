from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.documents.crud.awards import AwardCrud
from V2.app.core.documents.schemas.student_award import AwardFilterParams, AwardResponse



router = APIRouter()


@router.get("/", response_model=List[AwardResponse])
def get_archived_awards(filters: AwardFilterParams = Depends(),db: Session = Depends(get_db)):
    award_crud = AwardCrud(db)
    return award_crud.get_all_archived_awards(filters)


@router.get("/{award_id}", response_model=AwardResponse)
def get_archived_award(award_id: UUID, db: Session = Depends(get_db)):
    award_crud = AwardCrud(db)
    return award_crud.get_archived_award(award_id)


@router.patch("/{award_id}", response_model=AwardResponse)
def restore_award(award_id: UUID,db: Session = Depends(get_db)):
    award_crud = AwardCrud(db)
    return award_crud.restore_award(award_id)


@router.delete("/{award_id}", status_code=204)
def delete_archived_award(award_id: UUID, db: Session = Depends(get_db)):
    award_crud = AwardCrud(db)
    return award_crud.delete_archived_award(award_id)




