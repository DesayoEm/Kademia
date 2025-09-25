from uuid import UUID
from typing import List
from app.core.rbac.factories.permission import PermissionFactory
from app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from app.core.rbac.schemas.permissions import (
    PermissionFilterParams, PermissionResponse, PermissionCreate, PermissionUpdate, PermissionAudit
)
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


# Archived permissions
@router.get("/archive/permission/", response_model=List[PermissionResponse])
def get_archived_permission(
        filters: PermissionFilterParams = Depends(),
        factory: PermissionFactory = Depends(get_authenticated_factory(PermissionFactory))
):
    return factory.get_all_archived_permissions(filters)


@router.get("/archive/permission/{permission_id}/audit", response_model=PermissionAudit)
def get_archived_permission_audit(
        permission_id: UUID,
        factory: PermissionFactory = Depends(get_authenticated_factory(PermissionFactory))
):
    return factory.get_archived_permission(permission_id)


@router.get("/archive/permissions/{permission_id}", response_model=PermissionResponse)
def get_archived_permission(
        permission_id: UUID,
        factory: PermissionFactory = Depends(get_authenticated_factory(PermissionFactory))
):
    return factory.get_archived_permission(permission_id)


@router.patch("/archive/permissions/{permission_id}", response_model=PermissionResponse)
def restore_permission(
        permission_id: UUID,
        factory: PermissionFactory = Depends(get_authenticated_factory(PermissionFactory))
):
    return factory.restore_permission(permission_id)


@router.delete("/archive/permissions/{permission_id}", status_code=204)
def delete_archived_permission(
        permission_id: UUID,
        factory: PermissionFactory = Depends(get_authenticated_factory(PermissionFactory))
):
    return factory.delete_archived_permission(permission_id)


# Active permission Changes

@router.post("/permissions")
def create_permission(
        payload: PermissionCreate,
        factory: PermissionFactory = Depends(get_authenticated_factory(PermissionFactory))
):
    return factory.create_permission(payload)


@router.put("/permissions/{permission_id}", response_model=PermissionResponse)
def update_permission(
        payload: PermissionUpdate,
        award_id: UUID,
        factory: PermissionFactory = Depends(get_authenticated_factory(PermissionFactory))
):
    payload = payload.model_dump(exclude_unset=True)
    return factory.update_permission(award_id, payload)


@router.get("/permissions/", response_model=List[PermissionResponse])
def get_permission(
        filters: PermissionFilterParams = Depends(),
        factory: PermissionFactory = Depends(get_authenticated_factory(PermissionFactory))
):
    return factory.get_all_permissions(filters)



@router.get("/permissions/{permission_id}/audit", response_model=PermissionAudit)
def get_permission_audit(
        permission_id: UUID,
        factory: PermissionFactory = Depends(get_authenticated_factory(PermissionFactory))

):
    return factory.get_permission(permission_id)


@router.get("/permissions/{permission_id}", response_model=PermissionResponse)
def get_permission(
        permission_id: UUID,
        factory: PermissionFactory = Depends(get_authenticated_factory(PermissionFactory))

):
    return factory.get_all_permissions(permission_id)



@router.patch("/permissions/{permission_id}",  status_code=204)
def archive_permission(
        permission_id: UUID,
        reason:ArchiveRequest,
        factory: PermissionFactory = Depends(get_authenticated_factory(PermissionFactory))
):
    return factory.archive_permission(permission_id, reason.reason)


@router.delete("/permissions/{permission_id}", status_code=204)
def delete_permission(
        permission_id: UUID,
        factory: PermissionFactory = Depends(get_authenticated_factory(PermissionFactory))
):
    return factory.delete_permission(permission_id)










