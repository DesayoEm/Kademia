from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.responses import FileResponse
from ...schemas.enums import ExportFormat
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
def create_role(payload:StaffRoleCreate,db: Session = Depends(get_db)):
        roles_crud = StaffRoleCrud(db)
        return roles_crud.create_role(payload)


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
def update_role(payload: StaffRoleUpdate, role_id: UUID,
                         db: Session = Depends(get_db)):
        roles_crud = StaffRoleCrud(db)
        return roles_crud.update_role(role_id, payload)


@router.patch("/{role_id}", status_code=204)
def archive_role(role_id: UUID, reason:ArchiveRequest,
                          db: Session = Depends(get_db)):
        roles_crud = StaffRoleCrud(db)
        return roles_crud.archive_role(role_id, reason.reason)


@router.post("/{role_id}", response_class=FileResponse,  status_code=204)
def export_role(role_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    roles_crud = StaffRoleCrud(db)
    file_path= roles_crud.export_role(role_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{role_id}", status_code=204)
def delete_role(role_id: UUID, db: Session = Depends(get_db)):
        roles_crud = StaffRoleCrud(db)
        return roles_crud.delete_role(role_id)


