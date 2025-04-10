from sqlalchemy.orm import Session
from uuid import UUID

from ...core.services.export_service.export import ExportService
from ...database.models import StaffRole
from ...database.models.enums import ArchiveReason
from fastapi.responses import FileResponse
from ...schemas.staff_organization.role import (
    StaffRoleCreate, StaffRoleUpdate, RolesFilterParams, StaffRoleResponse
)
from fastapi import Depends, APIRouter
from ...database.session import get_db
from ...crud.staff_organization.staff_role import StaffRoleCrud
from ...schemas.shared_models import ArchiveRequest, ExportRequest
from fastapi import Query
from typing import Annotated


router = APIRouter()

@router.post("/", response_model= StaffRoleResponse, status_code = 201)
def create_role(data:StaffRoleCreate,db: Session = Depends(get_db)):
        roles_crud = StaffRoleCrud(db)
        return roles_crud.create_role(data)


@router.get("/", response_model=list[StaffRoleResponse])
def get_roles(filters: Annotated[RolesFilterParams, Query()],
                db: Session = Depends(get_db)):
        roles_crud = StaffRoleCrud(db)
        return roles_crud.get_all_roles(filters)


@router.get("/{role_id}", response_model=StaffRoleResponse)
def get_role(role_id: UUID, db: Session = Depends(get_db)):
        roles_crud = StaffRoleCrud(db)
        return roles_crud.get_role(role_id)


@router.put("/{role_id}", response_model=StaffRoleResponse)
def update_role(data: StaffRoleUpdate, role_id: UUID,
                         db: Session = Depends(get_db)):
        roles_crud = StaffRoleCrud(db)
        return roles_crud.update_role(role_id, data)


@router.patch("/{role_id}", status_code=204)
def archive_role(role_id: UUID, reason:ArchiveRequest,
                          db: Session = Depends(get_db)):
        roles_crud = StaffRoleCrud(db)
        return roles_crud.archive_role(role_id, reason.reason)


@router.delete("/{role_id}", status_code=204)
def delete_role(role_id: UUID, db: Session = Depends(get_db)):
        roles_crud = StaffRoleCrud(db)
        return roles_crud.delete_role(role_id)


# @router.post("/{role_id}", response_class=FileResponse)
# def export_entity(request: ExportRequest, db: Session = Depends(get_db)):
#
#     export_service = ExportService(db)
#
#     # Map entity_type string to actual model
#     model_map = {
#         "staffrole": StaffRole,
#     }
#
#     entity_model = model_map.get(request.entity_type.lower())
#
#     if not entity_model:
#         raise ValueError(f"Unsupported entity type: {request.entity_type}")
#
#     file_path = export_service.export_entity(entity_model, request.entity_id, request.export_format.value)
#
#     return FileResponse(
#         path=file_path,
#         filename=file_path.split("/")[-1],
#         media_type="application/octet-stream"
#     )
#
#
#
#
#
#


