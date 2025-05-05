from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from uuid import UUID
from V2.app.core.auth.schemas.access_level_change import AccessLevelFilterParams, AccessLevelChangeResponse
from V2.app.infra.db.session_manager import get_db
from V2.app.core.auth.crud.access_level_change import AccessLevelChangeCrud


router = APIRouter()


@router.get("/", response_model=list[AccessLevelChangeResponse])
def get_archived_level_changes(filters: AccessLevelFilterParams = Depends(),db: Session = Depends(get_db)):
    level_change_crud = AccessLevelChangeCrud(db)
    return level_change_crud.get_all_archived_access_level_changes(filters)


@router.get("/{level_change_id}", response_model=AccessLevelChangeResponse)
def get_archived_level_change(level_change_id: UUID, db: Session = Depends(get_db)):
    level_change_crud = AccessLevelChangeCrud(db)
    return level_change_crud.get_archived_access_level_change(level_change_id)


@router.patch("/{level_change_id}", response_model=AccessLevelChangeResponse)
def restore_level_change(level_change_id: UUID,db: Session = Depends(get_db)):
    level_change_crud = AccessLevelChangeCrud(db)
    return level_change_crud.restore_access_level_change(level_change_id)


@router.delete("/{level_change_id}", status_code=204)
def delete_archived_level_change(level_change_id: UUID, db: Session = Depends(get_db)):
    level_change_crud = AccessLevelChangeCrud(db)
    return level_change_crud.delete_archived_access_level_change(level_change_id)




