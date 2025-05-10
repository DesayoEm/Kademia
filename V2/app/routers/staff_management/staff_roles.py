from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.responses import FileResponse
from typing import List
from fastapi import Depends, APIRouter
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.staff_management.crud.staff_role import StaffRoleCrud
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from V2.app.core.staff_management.schemas.role import (
    StaffRoleCreate, StaffRoleUpdate, RolesFilterParams, StaffRoleResponse
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud, get_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("/", response_model= StaffRoleResponse, status_code = 201)
def create_role(
        payload:StaffRoleCreate,
        crud: StaffRoleCrud = Depends(get_authenticated_crud(StaffRoleCrud))
    ):
        return crud.create_role(payload)


@router.get("/", response_model= List[StaffRoleResponse])
def get_roles(
        filters: RolesFilterParams = Depends(),
        crud: StaffRoleCrud = Depends(get_authenticated_crud(StaffRoleCrud))
    ):
        return crud.get_all_roles(filters)


@router.get("/{role_id}", response_model=StaffRoleResponse)
def get_role(
        role_id: UUID,
        crud: StaffRoleCrud = Depends(get_authenticated_crud(StaffRoleCrud))
    ):
        return crud.get_role(role_id)


@router.put("/{role_id}", response_model=StaffRoleResponse)
def update_role(
        payload: StaffRoleUpdate,
        role_id: UUID,
        crud: StaffRoleCrud = Depends(get_authenticated_crud(StaffRoleCrud))
    ):
        return crud.update_role(role_id, payload)


@router.patch("/{role_id}", status_code=204)
def archive_role(
        role_id: UUID,
        reason:ArchiveRequest,
        crud: StaffRoleCrud = Depends(get_authenticated_crud(StaffRoleCrud))
    ):
        return crud.archive_role(role_id, reason.reason)


@router.post("/{role_id}", response_class=FileResponse,  status_code=204)
def export_role(
        role_id: UUID,
        export_format: ExportFormat,
        crud: StaffRoleCrud = Depends(get_authenticated_crud(StaffRoleCrud))
    ):
    file_path= crud.export_role(role_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{role_id}", status_code=204)
def delete_role(
        role_id: UUID,
        crud: StaffRoleCrud = Depends(get_authenticated_crud(StaffRoleCrud))
    ):
        return crud.delete_role(role_id)


