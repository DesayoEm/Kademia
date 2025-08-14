from uuid import UUID
from typing import List
from app.core.rbac.factories.role_history_factory import RoleHistoryFactory
from app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from app.core.rbac.schemas.staff_role_history import (
    RoleHistoryFilterParams, RoleHistoryResponse, RoleHistoryAudit
)
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


# Archived Access Level Changes
@router.get("/archive/role_history/", response_model=List[RoleHistoryResponse])
def get_archived_role_history(
        filters: RoleHistoryFilterParams = Depends(),
        factory: RoleHistoryFactory = Depends(get_authenticated_factory(RoleHistoryFactory))
):
    return factory.get_all_archived_role_changes(filters)


@router.get("/archive/role_history/{permissions_change_id}/audit", response_model=RoleHistoryAudit)
def get_archived_role_change_audit(
        role_change_id: UUID,
        factory: RoleHistoryFactory = Depends(get_authenticated_factory(RoleHistoryFactory))
):
    return factory.get_archived_role_change(role_change_id)


@router.get("/archive/permission_changes/{permissions_change_id}", response_model=RoleHistoryResponse)
def get_archived_role_change(
        role_change_id: UUID,
        factory: RoleHistoryFactory = Depends(get_authenticated_factory(RoleHistoryFactory))
):
    return factory.get_archived_role_change(role_change_id)


@router.patch("/archive/permission_changes/{permissions_change_id}", response_model=RoleHistoryResponse)
def restore_role_change(
        role_change_id: UUID,
        factory: RoleHistoryFactory = Depends(get_authenticated_factory(RoleHistoryFactory))
):
    return factory.restore_role_change(role_change_id)


@router.delete("/archive/permission_changes/{permissions_change_id}", status_code=204)
def delete_archived_role_change(
        role_change_id: UUID,
        factory: RoleHistoryFactory = Depends(get_authenticated_factory(RoleHistoryFactory))
):
    return factory.delete_archived_role_change(role_change_id)


# Active role Changes
@router.get("/permission_changes/", response_model=List[RoleHistoryResponse])
def get_role_history(
        filters: RoleHistoryFilterParams = Depends(),
        factory: RoleHistoryFactory = Depends(get_authenticated_factory(RoleHistoryFactory))
):
    return factory.get_all_role_changes(filters)



@router.get("/permission_changes/{permissions_change_id}/audit", response_model=RoleHistoryAudit)
def get_role_change_audit(
        role_change_id: UUID,
        factory: RoleHistoryFactory = Depends(get_authenticated_factory(RoleHistoryFactory))

):
    return factory.get_role_change(role_change_id)


@router.get("/permission_changes/{permissions_change_id}", response_model=RoleHistoryResponse)
def get_role_change(
        role_change_id: UUID,
        factory: RoleHistoryFactory = Depends(get_authenticated_factory(RoleHistoryFactory))

):
    return factory.get_all_role_changes(role_change_id)



@router.patch("/permission_changes/{permissions_change_id}",  status_code=204)
def archive_role_change(
        role_change_id: UUID,
        reason:ArchiveRequest,
        factory: RoleHistoryFactory = Depends(get_authenticated_factory(RoleHistoryFactory))
):
    return factory.archive_role_change(role_change_id, reason.reason)


@router.delete("/permission_changes/{permissions_change_id}", status_code=204)
def delete_role_change(
        role_change_id: UUID,
        factory: RoleHistoryFactory = Depends(get_authenticated_factory(RoleHistoryFactory))
):
    return factory.delete_role_change(role_change_id)










