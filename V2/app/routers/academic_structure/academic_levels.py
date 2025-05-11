
from uuid import UUID
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.core.academic_structure.crud.academic_levels import AcademicLevelCrud
from V2.app.core.academic_structure.schemas.academic_level import(
    AcademicLevelCreate, AcademicLevelUpdate, AcademicLevelFilterParams, AcademicLevelResponse
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/", response_model= AcademicLevelResponse, status_code=201)
def create_level(
        payload:AcademicLevelCreate,
        crud: AcademicLevelCrud = Depends(get_authenticated_crud(AcademicLevelCrud))
    ):
    return crud.create_level(payload)


@router.get("/", response_model=list[AcademicLevelResponse])
def get_levels(
        filters: AcademicLevelFilterParams = Depends(),
        crud: AcademicLevelCrud = Depends(get_authenticated_crud(AcademicLevelCrud))
    ):
    return crud.get_all_levels(filters)


@router.get("/{level_id}", response_model=AcademicLevelResponse)
def get_level(
        level_id: UUID, 
        crud: AcademicLevelCrud = Depends(get_authenticated_crud(AcademicLevelCrud))
    ):
    return crud.get_level(level_id)


@router.put("/{level_id}", response_model=AcademicLevelResponse)
def update_level(
        payload: AcademicLevelUpdate, level_id: UUID,
        crud: AcademicLevelCrud = Depends(get_authenticated_crud(AcademicLevelCrud))
    ):
    return crud.update_level(level_id, payload)


@router.patch("/{level_id}",  status_code=204)
def archive_level(
        level_id: UUID, reason:ArchiveRequest,
        crud: AcademicLevelCrud = Depends(get_authenticated_crud(AcademicLevelCrud))
    ):
    return crud.archive_level(level_id, reason.reason)


@router.post("/{level_id}", response_class=FileResponse,  status_code=204)
def export_level(
        level_id: UUID, 
        export_format: ExportFormat, 
        crud: AcademicLevelCrud = Depends(get_authenticated_crud(AcademicLevelCrud))
    ):
    file_path= crud.export_level(level_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{level_id}", status_code=204)
def delete_level(
        level_id: UUID, 
        crud: AcademicLevelCrud = Depends(get_authenticated_crud(AcademicLevelCrud))
    ):
    return crud.delete_level(level_id)










