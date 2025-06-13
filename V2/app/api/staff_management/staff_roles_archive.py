from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter

from V2.app.core.staff_management.factories.staff_role import StaffRoleFactory
from V2.app.core.staff_management.schemas.role import RolesFilterParams, StaffRoleResponse, StaffRoleAudit


from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer


token_service = TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[StaffRoleResponse])
def get_archived_roles(
        filters: RolesFilterParams = Depends(),
        factory: StaffRoleFactory = Depends(get_authenticated_factory(StaffRoleFactory))
    ):
    return factory.get_all_archived_roles(filters)


@router.get("/{role_id}/audit", response_model=StaffRoleAudit)
def get_archived_staff_role_audit(
        role_id: UUID,
        factory: StaffRoleFactory = Depends(get_authenticated_factory(StaffRoleFactory))
    ):
    """Get an archived role audit by ID."""
    return factory.get_archived_role(role_id)


@router.get("/{role_id}", response_model=StaffRoleResponse)
def get_archived_role(
        role_id: UUID,
        factory: StaffRoleFactory = Depends(get_authenticated_factory(StaffRoleFactory))
    ):
    return factory.get_archived_role(role_id)


@router.patch("/{role_id}", response_model=StaffRoleResponse)
def restore_role(
        role_id: UUID,
        factory: StaffRoleFactory = Depends(get_authenticated_factory(StaffRoleFactory))
    ):
    return factory.restore_role(role_id)


@router.delete("/{role_id}", status_code=204)
def delete_archived_role(
        role_id: UUID,
        factory: StaffRoleFactory = Depends(get_authenticated_factory(StaffRoleFactory))
    ):
    return factory.delete_archived_role(role_id)










