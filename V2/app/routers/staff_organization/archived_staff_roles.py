from sqlalchemy.orm import Session
from uuid import UUID
from ...database.models.data_enums import ArchiveReason
from ...schemas.staff_organization.role import RolesFilterParams, StaffRoleResponse
from fastapi import Depends, APIRouter
from ...database.session_manager import get_db
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
def delete_archived_role(role_id: UUID, db: Session = Depends(get_db)):
    roles_crud = StaffRoleCrud(db)
    return roles_crud.delete_archived_role(role_id)














