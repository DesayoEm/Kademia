
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse
from fastapi import Depends, APIRouter

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.identity.schemas.guardian import (
    GuardianCreate, GuardianUpdate, GuardianResponse, GuardianFilterParams
)

from V2.app.core.identity.crud.guardian import GuardianCrud
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("/", response_model= GuardianResponse, status_code=201)
def create_guardian(
        data:GuardianCreate,
        crud: GuardianCrud = Depends(get_authenticated_crud(GuardianCrud))
    ):
        return crud.create_guardian(data)


@router.get("/", response_model=List[GuardianResponse])
def get_guardians(
        filters: GuardianFilterParams = Depends(),
        crud: GuardianCrud = Depends(get_authenticated_crud(GuardianCrud))
    ):
        return crud.get_all_guardians(filters)


@router.get("/{guardian_id}", response_model=GuardianResponse)
def get_guardian(
        guardian_id: UUID, 
        crud: GuardianCrud = Depends(get_authenticated_crud(GuardianCrud))
    ):
        return crud.get_guardian(guardian_id)


@router.put("/{guardian_id}", response_model=GuardianResponse)
def update_guardian(
        data: GuardianUpdate, 
        guardian_id: UUID,
        crud: GuardianCrud = Depends(get_authenticated_crud(GuardianCrud))
    ):
        return crud.update_guardian(guardian_id, data)


@router.patch("/{guardian_id}", status_code=204)
def archive_guardian(
        guardian_id: UUID, 
        reason:ArchiveRequest,
        crud: GuardianCrud = Depends(get_authenticated_crud(GuardianCrud))
    ):
        return crud.archive_guardian(guardian_id, reason.reason)


@router.post("/{guardian_id}", response_class=FileResponse,  status_code=204)
def export_guardian(
        guardian_id: UUID, 
        export_format: ExportFormat, 
        crud: GuardianCrud = Depends(get_authenticated_crud(GuardianCrud))
    ):
    file_path= crud.export_guardian(guardian_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{guardian_id}", status_code=204)
def delete_guardian(
        guardian_id: UUID, crud: GuardianCrud = Depends(get_authenticated_crud(GuardianCrud))
    ):
        return crud.delete_guardian(guardian_id)











