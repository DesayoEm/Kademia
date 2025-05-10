from fastapi import Depends, APIRouter
from uuid import UUID
from V2.app.core.auth.schemas.access_level_change import AccessLevelFilterParams, AccessLevelChangeResponse
from V2.app.core.auth.crud.access_level_change import AccessLevelChangeCrud
from V2.app.core.auth.services.dependencies.current_user_deps import get_crud

router = APIRouter()


@router.get("/", response_model=list[AccessLevelChangeResponse])
def get_archived_level_changes(
        filters: AccessLevelFilterParams = Depends(),
        crud: AccessLevelChangeCrud = Depends(get_crud(AccessLevelChangeCrud))
):
    return crud.get_all_archived_access_level_changes(filters)


@router.get("/{level_change_id}", response_model=AccessLevelChangeResponse)
def get_archived_level_change(
        level_change_id: UUID,
        crud: AccessLevelChangeCrud = Depends(get_crud(AccessLevelChangeCrud))
):
    return crud.get_archived_access_level_change(level_change_id)


@router.patch("/{level_change_id}", response_model=AccessLevelChangeResponse)
def restore_level_change(
        level_change_id: UUID,
        crud: AccessLevelChangeCrud = Depends(get_crud(AccessLevelChangeCrud))
):
    return crud.restore_access_level_change(level_change_id)


@router.delete("/{level_change_id}", status_code=204)
def delete_archived_level_change(
        level_change_id: UUID,
        crud: AccessLevelChangeCrud = Depends(get_crud(AccessLevelChangeCrud))
):
    return crud.delete_archived_access_level_change(level_change_id)




