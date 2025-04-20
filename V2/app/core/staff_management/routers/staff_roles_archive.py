from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import Query
from typing import Annotated
from fastapi import Depends, APIRouter

from V2.app.core.shared.database.session_manager import get_db
from V2.app.core.staff_management.crud.staff_role import StaffRoleCrud
from V2.app.core.staff_management.schemas.role import RolesFilterParams, StaffRoleResponse


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










