
from fastapi import Depends, APIRouter
from uuid import UUID

from V2.app.core.academic_structure.schemas.academic_level import(
    AcademicLevelFilterParams, AcademicLevelResponse
)

from V2.app.core.academic_structure.crud.academic_levels import AcademicLevelCrud
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=list[AcademicLevelResponse])
def get_archived_levels(
        filters: AcademicLevelFilterParams = Depends(),
        crud: AcademicLevelCrud = Depends(get_authenticated_crud(AcademicLevelCrud))
):
    return crud.get_all_archived_levels(filters)


@router.get("/{level_id}", response_model=AcademicLevelResponse)
def get_archived_level(
        level_id: UUID,
        crud: AcademicLevelCrud = Depends(get_authenticated_crud(AcademicLevelCrud))
    ):
    return crud.get_archived_level(level_id)


@router.patch("/{level_id}", response_model=AcademicLevelResponse)
def restore_level(
        level_id: UUID,
        crud: AcademicLevelCrud = Depends(get_authenticated_crud(AcademicLevelCrud))
    ):
    return crud.restore_level(level_id)


@router.delete("/{level_id}", status_code=204)
def delete_archived_level(
        level_id: UUID,
        crud: AcademicLevelCrud = Depends(get_authenticated_crud(AcademicLevelCrud))
    ):
    return crud.delete_archived_level(level_id)




