from uuid import UUID
from typing import List
from app.core.rbac.factories.role import RoleFactory
from app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from app.core.rbac.schemas.roles import (
    RoleFilterParams, RoleResponse, RoleCreate, RoleUpdate, RoleAudit
)
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


# Archived roles
@router.get("/archive/role/", response_model=List[RoleResponse])
def get_archived_role(
        filters: RoleFilterParams = Depends(),
        factory: RoleFactory = Depends(get_authenticated_factory(RoleFactory))
):
    return factory.get_all_archived_roles(filters)


@router.get("/archive/role/{role_id}/audit", response_model=RoleAudit)
def get_archived_role_audit(
        role_id: UUID,
        factory: RoleFactory = Depends(get_authenticated_factory(RoleFactory))
):
    return factory.get_archived_role(role_id)


@router.get("/archive/roles/{role_id}", response_model=RoleResponse)
def get_archived_role(
        role_id: UUID,
        factory: RoleFactory = Depends(get_authenticated_factory(RoleFactory))
):
    return factory.get_archived_role(role_id)


@router.patch("/archive/roles/{role_id}", response_model=RoleResponse)
def restore_role(
        role_id: UUID,
        factory: RoleFactory = Depends(get_authenticated_factory(RoleFactory))
):
    return factory.restore_role(role_id)


@router.delete("/archive/roles/{role_id}", status_code=204)
def delete_archived_role(
        role_id: UUID,
        factory: RoleFactory = Depends(get_authenticated_factory(RoleFactory))
):
    return factory.delete_archived_role(role_id)


# Active role Changes

@router.post("/roles")
def create_role(
        payload: RoleCreate,
        factory: RoleFactory = Depends(get_authenticated_factory(RoleFactory))
):
    return factory.create_role(payload)


@router.put("/roles/{role_id}", response_model=RoleResponse)
def update_role(
        payload: RoleUpdate,
        award_id: UUID,
        factory: RoleFactory = Depends(get_authenticated_factory(RoleFactory))
):
    payload = payload.model_dump(exclude_unset=True)
    return factory.update_role(award_id, payload)


@router.get("/roles/", response_model=List[RoleResponse])
def get_role(
        filters: RoleFilterParams = Depends(),
        factory: RoleFactory = Depends(get_authenticated_factory(RoleFactory))
):
    return factory.get_all_roles(filters)



@router.get("/roles/{role_id}/audit", response_model=RoleAudit)
def get_role_audit(
        role_id: UUID,
        factory: RoleFactory = Depends(get_authenticated_factory(RoleFactory))

):
    return factory.get_role(role_id)


@router.get("/roles/{role_id}", response_model=RoleResponse)
def get_role(
        role_id: UUID,
        factory: RoleFactory = Depends(get_authenticated_factory(RoleFactory))

):
    return factory.get_all_roles(role_id)



@router.patch("/roles/{role_id}",  status_code=204)
def archive_role(
        role_id: UUID,
        reason:ArchiveRequest,
        factory: RoleFactory = Depends(get_authenticated_factory(RoleFactory))
):
    return factory.archive_role(role_id, reason.reason)


@router.delete("/roles/{role_id}", status_code=204)
def delete_role(
        role_id: UUID,
        factory: RoleFactory = Depends(get_authenticated_factory(RoleFactory))
):
    return factory.delete_role(role_id)










