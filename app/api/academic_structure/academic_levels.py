
from uuid import UUID
from fastapi.responses import FileResponse

from app.core.academic_structure.services.academic_structure import AcademicStructureService
from app.core.shared.schemas.enums import ExportFormat
from app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service
from app.core.academic_structure.factories.academic_level import AcademicLevelFactory
from app.core.academic_structure.schemas.academic_level import(
    AcademicLevelCreate, AcademicLevelUpdate, AcademicLevelFilterParams, AcademicLevelResponse,
    AcademicLevelAudit
)
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/", response_model= AcademicLevelResponse, status_code=201)
def create_level(
        payload:AcademicLevelCreate,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.create_academic_level(payload)


@router.get("/", response_model=list[AcademicLevelResponse])
def get_levels(
        filters: AcademicLevelFilterParams = Depends(),
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.get_all_academic_levels(filters)

@router.get("/{level_id}/audit", response_model=AcademicLevelAudit)
def get_level_audit(
        level_id: UUID,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.get_academic_level(level_id)


@router.get("/{level_id}", response_model=AcademicLevelResponse)
def get_level(
        level_id: UUID, 
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.get_academic_level(level_id)


@router.put("/{level_id}", response_model=AcademicLevelResponse)
def update_level(
        payload: AcademicLevelUpdate, level_id: UUID,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    update_data = payload.model_dump(exclude_unset=True)
    return factory.update_academic_level(level_id, update_data)


@router.patch("/{level_id}",  status_code=204)
def archive_level(
        level_id: UUID, reason:ArchiveRequest,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.archive_academic_level(level_id, reason.reason)


@router.post("/{level_id}", response_class=FileResponse,  status_code=204)
def export_level(
        level_id: UUID, 
        export_format: ExportFormat, 
        service: AcademicStructureService = Depends(get_authenticated_service(AcademicStructureService))
    ):
    file_path= service.export_academic_level(level_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{level_id}", status_code=204)
def delete_level(
        level_id: UUID, 
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.delete_academic_level(level_id)










