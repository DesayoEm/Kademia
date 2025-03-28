from sqlalchemy.orm import Session
from uuid import UUID
from ....schemas.users.guardian import GuardianResponse, GuardianFilterParams
from fastapi import Depends, APIRouter
from ....database.session import get_db
from ....crud.users.guardian import GuardianCrud
from fastapi import Query
from typing import Annotated

router = APIRouter()

@router.get("/", response_model=list[GuardianResponse])
def get_archived_guardians(filters: Annotated[GuardianFilterParams, Query()],
        db: Session = Depends(get_db)):
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











