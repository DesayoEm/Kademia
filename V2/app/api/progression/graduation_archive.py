from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from V2.app.core.progression.factories.graduation import GraduationFactory
from V2.app.core.progression.schemas.graduation import (
    GraduationResponse,
    GraduationFilterParams,
    GraduationAudit
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[GraduationResponse])
def get_all_archived_graduations(
        filters: GraduationFilterParams = Depends(),
        factory: GraduationFactory = Depends(get_authenticated_factory(GraduationFactory))
    ):
    return factory.get_all_archived_graduations(filters)


@router.get("/{graduation_id}/audit", response_model=GraduationAudit)
def get_archived_graduation_audit(
        graduation_id: UUID,
        factory: GraduationFactory = Depends(get_authenticated_factory(GraduationFactory))
    ):
    return factory.get_archived_graduation(graduation_id)


@router.get("/{graduation_id}", response_model=GraduationResponse)
def get_archived_graduation(
        graduation_id: UUID,
        factory: GraduationFactory = Depends(get_authenticated_factory(GraduationFactory))
    ):
    return factory.get_archived_graduation(graduation_id)


@router.patch("/{graduation_id}", response_model=GraduationResponse)
def restore_graduation(
        graduation_id: UUID,
        factory: GraduationFactory = Depends(get_authenticated_factory(GraduationFactory))
    ):
    return factory.restore_graduation(graduation_id)


@router.delete("/{graduation_id}", status_code=204)
def delete_archived_graduation(
        graduation_id: UUID,
        factory: GraduationFactory = Depends(get_authenticated_factory(GraduationFactory))
    ):
    return factory.delete_archived_graduation(graduation_id)
