from sqlalchemy.orm import Session
from uuid import UUID
from ....schemas.users.guardian import GuardianCreate, GuardianUpdate, GuardianResponse, GuardianFilterParams
from fastapi import Depends, APIRouter
from ....database.session_manager import get_db
from ....crud.users.guardian import GuardianCrud
from ....schemas.shared_models import ArchiveRequest
from fastapi import Query
from typing import Annotated

router = APIRouter()


@router.post("/", response_model= GuardianResponse, status_code=201)
def create_guardian(data:GuardianCreate,
                db: Session = Depends(get_db)):
        guardian_crud = GuardianCrud(db)
        return guardian_crud.create_guardian(data)


@router.get("/", response_model=list[GuardianResponse])
def get_guardians(filters: Annotated[GuardianFilterParams, Query()],
                db: Session = Depends(get_db)):
        guardian_crud = GuardianCrud(db)
        return guardian_crud.get_all_guardians(filters)


@router.get("/{guardian_id}", response_model=GuardianResponse)
def get_guardian(guardian_id: UUID, db: Session = Depends(get_db)):
        guardian_crud = GuardianCrud(db)
        return guardian_crud.get_guardian(guardian_id)


@router.put("/{guardian_id}", response_model=GuardianResponse)
def update_guardian(data: GuardianUpdate, guardian_id: UUID,
                         db: Session = Depends(get_db)):
        guardian_crud = GuardianCrud(db)
        return guardian_crud.update_guardian(guardian_id, data)


@router.patch("/{guardian_id}", status_code=204)
def archive_guardian(guardian_id: UUID, reason:ArchiveRequest,
                          db: Session = Depends(get_db)):
        guardian_crud = GuardianCrud(db)
        return guardian_crud.archive_guardian(guardian_id, reason.reason)


@router.delete("/{guardian_id}", status_code=204)
def delete_guardian(guardian_id: UUID, db: Session = Depends(get_db)):
        guardian_crud = GuardianCrud(db)
        return guardian_crud.delete_guardian(guardian_id)











