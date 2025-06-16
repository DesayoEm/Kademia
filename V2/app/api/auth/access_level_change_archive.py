from fastapi import Depends, APIRouter
from uuid import UUID

from V2.app.core.auth.factories.access_level_factory import AccessLevelChangeFactory
from typing import List 
from V2.app.core.auth.schemas.access_level_change import AccessLevelFilterParams, AccessLevelChangeResponse, \
    AccessLevelChangeAudit
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

router = APIRouter()


@router.get("/", response_model=List[AccessLevelChangeResponse])
def get_archived_level_changes(
        filters: AccessLevelFilterParams = Depends(),
        factory: AccessLevelChangeFactory = Depends(get_authenticated_factory(AccessLevelChangeFactory))
):
    return factory.get_all_archived_level_changes(filters)

@router.get("/{level_change_id}/Audit", response_model=AccessLevelChangeAudit)
def get_archived_level_change_audit(
        level_change_id: UUID,
        factory: AccessLevelChangeFactory = Depends(get_authenticated_factory(AccessLevelChangeFactory))
):
    return factory.get_archived_level_change(level_change_id)


@router.get("/{level_change_id}", response_model=AccessLevelChangeResponse)
def get_archived_level_change(
        level_change_id: UUID,
        factory: AccessLevelChangeFactory = Depends(get_authenticated_factory(AccessLevelChangeFactory))
):
    return factory.get_archived_level_change(level_change_id)


@router.patch("/{level_change_id}", response_model=AccessLevelChangeResponse)
def restore_level_change(
        level_change_id: UUID,
        factory: AccessLevelChangeFactory = Depends(get_authenticated_factory(AccessLevelChangeFactory))
):
    return factory.restore_level_change(level_change_id)


@router.delete("/{level_change_id}", status_code=204)
def delete_archived_level_change(
        level_change_id: UUID,
        factory: AccessLevelChangeFactory = Depends(get_authenticated_factory(AccessLevelChangeFactory))
):
    return factory.delete_archived_level_change(level_change_id)




