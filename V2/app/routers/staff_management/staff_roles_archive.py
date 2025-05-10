
from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter

from V2.app.core.staff_management.crud.staff_role import StaffRoleCrud
from V2.app.core.staff_management.schemas.role import RolesFilterParams, StaffRoleResponse
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[StaffRoleResponse])
def get_archived_roles(
        filters: RolesFilterParams = Depends(),
        crud: StaffRoleCrud = Depends(get_authenticated_crud(StaffRoleCrud))
    ):
    return crud.get_all_archived_roles(filters)


@router.get("/{role_id}", response_model=StaffRoleResponse)
def get_archived_role(
        role_id: UUID,
        crud: StaffRoleCrud = Depends(get_authenticated_crud(StaffRoleCrud))
    ):
    return crud.get_archived_role(role_id)


@router.patch("/{role_id}", response_model=StaffRoleResponse)
def restore_role(
        role_id: UUID,
        crud: StaffRoleCrud = Depends(get_authenticated_crud(StaffRoleCrud))
    ):
    return crud.restore_role(role_id)


@router.delete("/{role_id}", status_code=204)
def delete_archived_role(
        role_id: UUID,
        crud: StaffRoleCrud = Depends(get_authenticated_crud(StaffRoleCrud))
    ):
    return crud.delete_archived_role(role_id)










