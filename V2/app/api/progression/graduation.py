from fastapi import APIRouter, Depends

from uuid import UUID
from typing import List

from V2.app.core.progression.factories.graduation import GraduationFactory
from V2.app.core.progression.schemas.graduation import (
    GraduationCreate,
    GraduationResponse,
    GraduationFilterParams, GraduationAudit
)
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, get_authenticated_service

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/students/{student_id}", response_model=GraduationResponse, status_code=201)
def graduate_student(
        student_id: UUID,
        payload: GraduationCreate,
        factory: GraduationFactory = Depends(get_authenticated_factory(GraduationFactory))
    ):
    return factory.create_graduation(student_id, payload)


@router.get("/", response_model=List[GraduationResponse])
def get_all_graduations(
        filters: GraduationFilterParams = Depends(),
        factory: GraduationFactory = Depends(get_authenticated_factory(GraduationFactory))
    ):
    return factory.get_all_graduations(filters)



@router.get("/{graduation_id}/audit", response_model=GraduationAudit)
def get_graduation_audit(
        graduation_id: UUID,
        factory: GraduationFactory = Depends(get_authenticated_factory(GraduationFactory))
    ):
    return factory.get_graduation(graduation_id)


@router.get("/{graduation_id}", response_model=GraduationResponse)
def get_graduation(
        graduation_id: UUID,
        factory: GraduationFactory = Depends(get_authenticated_factory(GraduationFactory))
    ):
    return factory.get_graduation(graduation_id)


@router.patch("/{graduation_id}", status_code=204)
def archive_graduation(
        graduation_id: UUID,
        reason: ArchiveRequest,
        factory: GraduationFactory = Depends(get_authenticated_factory(GraduationFactory))
    ):
    return factory.archive_graduation(graduation_id, reason.reason)


@router.delete("/{graduation_id}", status_code=204)
def delete_graduation(
        graduation_id: UUID,
        factory: GraduationFactory = Depends(get_authenticated_factory(GraduationFactory))
    ):
    return factory.delete_graduation(graduation_id)
