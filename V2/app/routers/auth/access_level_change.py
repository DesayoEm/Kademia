from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.auth.crud.access_level_change import AccessLevelChangeCrud
from V2.app.core.auth.schemas.access_level_change import (
    AccessLevelChangeCreate, AccessLevelFilterParams, AccessLevelChangeResponse
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_current_user, get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()

@router.post("/{staff_id}", response_model=AccessLevelChangeResponse, status_code=201)
def change_access_level(
    staff_id: UUID,
    data: AccessLevelChangeCreate,
    crud: AccessLevelChangeCrud = Depends(get_authenticated_crud(AccessLevelChangeCrud))
):
    return crud.create_access_level_change(staff_id, data)


@router.get("/", response_model=list[AccessLevelChangeResponse])
def get_level_changes(filters: AccessLevelFilterParams = Depends(),db: Session = Depends(get_db)):
    level_change_crud = AccessLevelChangeCrud(db)
    return level_change_crud.get_all_access_level_changes(filters)


@router.get("/{level_change_id}", response_model=AccessLevelChangeResponse)
def get_level_change(level_change_id: UUID, db: Session = Depends(get_db)):
    level_change_crud = AccessLevelChangeCrud(db)
    return level_change_crud.get_access_level_change(level_change_id)


@router.patch("/{level_change_id}",  status_code=204)
def archive_level_change(level_change_id: UUID, reason:ArchiveRequest,
                       db: Session = Depends(get_db)):
    level_change_crud = AccessLevelChangeCrud(db)
    return level_change_crud.archive_access_level_change(level_change_id, reason.reason)


@router.get("/{level_change_id}/export", response_class=FileResponse,  status_code=204)
def export_level_change(level_change_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    level_change_crud = AccessLevelChangeCrud(db)
    file_path= level_change_crud.export_access_level_change(level_change_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{level_change_id}", status_code=204)
def delete_level_change(level_change_id: UUID, db: Session = Depends(get_db)):
    level_change_crud = AccessLevelChangeCrud(db)
    return level_change_crud.delete_access_level_change(level_change_id)










