from uuid import UUID
from fastapi.responses import FileResponse
from typing import List

from V2.app.core.auth.services.access_level_service import AccessLevelService
from V2.app.core.auth.factories.access_level_factory import AccessLevelChangeFactory
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.core.auth.schemas.access_level_change import (
    AccessLevelFilterParams, AccessLevelChangeResponse, AccessLevelChangeAudit
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[AccessLevelChangeResponse])
def get_level_changes(
        filters: AccessLevelFilterParams = Depends(),
        factory: AccessLevelChangeFactory = Depends(get_authenticated_factory(AccessLevelChangeFactory))
):
    return factory.get_all_level_changes(filters)



@router.get("/{level_change_id}/audit", response_model=AccessLevelChangeAudit)
def get_level_change_audit(
        level_change_id: UUID,
        factory: AccessLevelChangeFactory = Depends(get_authenticated_factory(AccessLevelChangeFactory))

):
    return factory.get_level_change(level_change_id)


@router.get("/{level_change_id}", response_model=AccessLevelChangeResponse)
def get_level_change(
        level_change_id: UUID,
        factory: AccessLevelChangeFactory = Depends(get_authenticated_factory(AccessLevelChangeFactory))

):
    return factory.get_level_change(level_change_id)



@router.patch("/{level_change_id}",  status_code=204)
def archive_level_change(
        level_change_id: UUID,
        reason:ArchiveRequest,
        factory: AccessLevelChangeFactory = Depends(get_authenticated_factory(AccessLevelChangeFactory))
):
    return factory.archive_level_change(level_change_id, reason.reason)


@router.get("/{level_change_id}/export", response_class=FileResponse,  status_code=204)
def export_level_change(
        level_change_id: UUID,
        export_format: ExportFormat,
        service: AccessLevelService = Depends(get_authenticated_service(AccessLevelService))
):
    file_path= service.export_access_level_change(level_change_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{level_change_id}", status_code=204)
def delete_level_change(
        level_change_id: UUID,
        factory: AccessLevelChangeFactory = Depends(get_authenticated_factory(AccessLevelChangeFactory))
):
    return factory.delete_level_change(level_change_id)










