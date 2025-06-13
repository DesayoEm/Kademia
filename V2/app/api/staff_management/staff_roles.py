from uuid import UUID
from fastapi.responses import FileResponse
from typing import List
from fastapi import Depends, APIRouter
from V2.app.core.shared.schemas.enums import ExportFormat

from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from V2.app.core.staff_management.factories.staff_role import StaffRoleFactory
from V2.app.core.staff_management.schemas.role import (
    StaffRoleCreate, StaffRoleUpdate, RolesFilterParams, StaffRoleResponse, StaffRoleAudit
)

from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service

from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.staff_management.services.staff_management import StaffManagementService

token_service = TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/", response_model= StaffRoleResponse, status_code = 201)
def create_role(
        payload:StaffRoleCreate,
        factory: StaffRoleFactory = Depends(get_authenticated_factory(StaffRoleFactory))
    ):
        return factory.create_role(payload)


@router.get("/", response_model= List[StaffRoleResponse])
def get_roles(
        filters: RolesFilterParams = Depends(),
        factory: StaffRoleFactory = Depends(get_authenticated_factory(StaffRoleFactory))
    ):
        return factory.get_all_roles(filters)


@router.get("/{role_id}/audit", response_model=StaffRoleAudit)
def get_staff_role_audit(
        role_id: UUID,
        factory: StaffRoleFactory = Depends(get_authenticated_factory(StaffRoleFactory))
    ):
    """Get a role audit by ID."""
    return factory.get_role(role_id)


@router.get("/{role_id}", response_model=StaffRoleResponse)
def get_role(
        role_id: UUID,
        factory: StaffRoleFactory = Depends(get_authenticated_factory(StaffRoleFactory))
    ):
        return factory.get_role(role_id)


@router.put("/{role_id}", response_model=StaffRoleResponse)
def update_role(
        payload: StaffRoleUpdate,
        role_id: UUID,
        factory: StaffRoleFactory = Depends(get_authenticated_factory(StaffRoleFactory))
    ):
        update_data = payload.model_dump(exclude_unset=True)
        return factory.update_role(role_id, update_data)


@router.patch("/{role_id}", status_code=204)
def archive_role(
        role_id: UUID,
        reason:ArchiveRequest,
        factory: StaffRoleFactory = Depends(get_authenticated_factory(StaffRoleFactory))
    ):
        return factory.archive_role(role_id, reason.reason)


@router.post("/{role_id}", response_class=FileResponse,  status_code=204)
def export_role(
        role_id: UUID,
        export_format: ExportFormat,
        service: StaffManagementService = Depends(get_authenticated_service(StaffManagementService))
    ):
    file_path= service.export_role(role_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{role_id}", status_code=204)
def delete_role(
        role_id: UUID,
        factory: StaffRoleFactory = Depends(get_authenticated_factory(StaffRoleFactory))
    ):
        return factory.delete_role(role_id)


