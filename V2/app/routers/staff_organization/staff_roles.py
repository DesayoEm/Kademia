from sqlalchemy.orm import Session
from uuid import UUID
from ...database.models.data_enums import ArchiveReason
from ...schemas.staff_organization.staff_roles import (
    StaffRoleCreate, StaffRoleUpdate, RolesFilterParams, StaffRoleResponse
)
from fastapi import Depends, APIRouter
from ...database.session_manager import get_db
from ...crud.staff_organization.staff_roles import StaffRoleCrud
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


@router.patch("/{role_id}", response_model=StaffRoleResponse)
def archive_role(role_id: UUID, reason:ArchiveReason,
                          db: Session = Depends(get_db)):
        roles_crud = StaffRoleCrud(db)
        return roles_crud.archive_role(role_id, reason)


@router.delete("/{role_id}", status_code=204)
def delete_role(role_id: UUID, db: Session = Depends(get_db)):
        roles_crud = StaffRoleCrud(db)
        return roles_crud.delete_role(role_id)














