from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.identity.schemas.guardian import GuardianResponse, GuardianFilterParams
from V2.app.core.identity.crud.guardian import GuardianCrud

router = APIRouter()

@router.get("/", response_model=list[GuardianResponse])
def get_archived_guardians(filters: GuardianFilterParams = Depends(),db: Session = Depends(get_db)):
    guardian_crud = GuardianCrud(db)
    return guardian_crud.get_all_archived_guardians(filters)


@router.get("/{guardian_id}", response_model=GuardianResponse)
def get_archived_guardian(guardian_id: UUID, db: Session = Depends(get_db)):
    guardian_crud = GuardianCrud(db)
    return guardian_crud.get_archived_guardian(guardian_id)


@router.patch("/{guardian_id}", response_model=GuardianResponse)
def restore_guardian(guardian_id: UUID, db: Session = Depends(get_db)):
    guardian_crud = GuardianCrud(db)
    return guardian_crud.restore_guardian(guardian_id)


@router.delete("/{guardian_id}", status_code=204)
def delete_archived_guardian(guardian_id: UUID, db: Session = Depends(get_db)):
    guardian_crud = GuardianCrud(db)
    return guardian_crud.delete_archived_guardian(guardian_id)











