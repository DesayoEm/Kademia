
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.core.documents.crud.awards import AwardCrud
from V2.app.core.documents.schemas.student_award import(
    AwardFilterParams, AwardCreate, AwardUpdate, AwardResponse
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("{student_id}/", response_model= AwardResponse, status_code=201)
def add_award(
        student_id: UUID,
        payload:AwardCreate,
        crud: AwardCrud = Depends(get_authenticated_crud(AwardCrud))
    ):
    return crud.create_award(student_id, payload)


@router.get("/", response_model=List[AwardResponse])
def get_awards(
        filters: AwardFilterParams = Depends(),
        crud: AwardCrud = Depends(get_authenticated_crud(AwardCrud))
    ):
    return crud.get_all_awards(filters)


@router.get("/{award_id}", response_model=AwardResponse)
def get_award(
        award_id: UUID,
        crud: AwardCrud = Depends(get_authenticated_crud(AwardCrud))
     ):
    return crud.get_award(award_id)


@router.put("/{award_id}", response_model=AwardResponse)
def update_award(
        payload: AwardUpdate,
        award_id: UUID,
        crud: AwardCrud = Depends(get_authenticated_crud(AwardCrud))
    ):
    return crud.update_award(award_id, payload)


@router.patch("/{award_id}",  status_code=204)
def archive_award(
        award_id: UUID,
        reason:ArchiveRequest,
        crud: AwardCrud = Depends(get_authenticated_crud(AwardCrud))
    ):
    return crud.archive_award(award_id, reason.reason)


@router.post("/{award_id}", response_class=FileResponse,  status_code=204)
def export_award(
        award_id: UUID,
        export_format: ExportFormat,
        crud: AwardCrud = Depends(get_authenticated_crud(AwardCrud))
):
    file_path= crud.export_award(award_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{award_id}", status_code=204)
def delete_award(
        award_id: UUID,
        crud: AwardCrud = Depends(get_authenticated_crud(AwardCrud))
):
    return crud.delete_award(award_id)










