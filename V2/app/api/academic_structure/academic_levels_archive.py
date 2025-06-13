
from fastapi import Depends, APIRouter
from uuid import UUID
from typing import List
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory
from V2.app.core.academic_structure.factories.academic_level import AcademicLevelFactory
from V2.app.core.academic_structure.schemas.academic_level import(
    AcademicLevelFilterParams, AcademicLevelResponse, AcademicLevelAudit
)

from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[AcademicLevelResponse])
def get_archived_levels(
        filters: AcademicLevelFilterParams = Depends(),
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
):
    return factory.get_all_archived_academic_levels(filters)


@router.get("/archived//{level_id}/audit", response_model=AcademicLevelAudit)
def get_archived_level_audit(
        level_id: UUID,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.get_archived_academic_level(level_id)


@router.get("/{level_id}", response_model=AcademicLevelResponse)
def get_archived_level(
        level_id: UUID,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.get_archived_academic_level(level_id)


@router.patch("/{level_id}", response_model=AcademicLevelResponse)
def restore_level(
        level_id: UUID,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.restore_academic_level(level_id)


@router.delete("/{level_id}", status_code=204)
def delete_archived_level(
        level_id: UUID,
        factory: AcademicLevelFactory = Depends(get_authenticated_factory(AcademicLevelFactory))
    ):
    return factory.delete_archived_academic_level(level_id)




