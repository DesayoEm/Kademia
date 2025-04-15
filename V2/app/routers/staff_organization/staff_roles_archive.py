from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.responses import FileResponse
from ...schemas.enums import ExportFormat
from ...schemas.staff_organization.role import RolesFilterParams, StaffRoleResponse
from fastapi import Depends, APIRouter
from ...database.session import get_db
from ...crud.staff_organization.staff_role import StaffRoleCrud
from fastapi import Query
from typing import Annotated

router = APIRouter()


@router.get("/", response_model=list[StaffRoleResponse])
def get_archived_roles(
        filters: Annotated[RolesFilterParams, Query()],
        db: Session = Depends(get_db)):
    roles_crud = StaffRoleCrud(db)
    return roles_crud.get_all_archived_roles(filters)


@router.get("/{role_id}", response_model=StaffRoleResponse)
def get_archived_role(role_id: UUID, db: Session = Depends(get_db)):
    roles_crud = StaffRoleCrud(db)
    return roles_crud.get_archived_role(role_id)


@router.patch("/{role_id}", response_model=StaffRoleResponse)
def restore_role(role_id: UUID,db: Session = Depends(get_db)):
    roles_crud = StaffRoleCrud(db)
    return roles_crud.restore_role(role_id)


@router.delete("/{role_id}", status_code=204)
def safe_delete_archived_role(role_id: UUID, db: Session = Depends(get_db)):
    roles_crud = StaffRoleCrud(db)
    return roles_crud.safe_delete_archived_role(role_id)


@router.delete("/{role_id}/force", response_class=FileResponse, status_code=204)
def force_delete_archived_role(role_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    roles_crud = StaffRoleCrud(db)

    file_path= roles_crud.force_delete_archived_role(role_id, export_format.value)
    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )













