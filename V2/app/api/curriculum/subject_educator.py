
from uuid import UUID
from typing import List

from V2.app.core.curriculum.factories.subject_educator import SubjectEducatorFactory
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter

from V2.app.core.curriculum.schemas.subject_educator import (
    SubjectEducatorCreate, SubjectEducatorFilterParams, SubjectEducatorResponse, SubjectEducatorAudit
)

from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("/{educator_id}", response_model= SubjectEducatorResponse, status_code=201)
def assign_subject_educator(
        educator_id: UUID,
        data:SubjectEducatorCreate,
        factory: SubjectEducatorFactory = Depends(get_authenticated_factory(SubjectEducatorFactory))
    ):
    return factory.create_subject_educator(educator_id,data)


@router.get("/", response_model=List[SubjectEducatorResponse])
def get_subject_educators(
        filters: SubjectEducatorFilterParams = Depends(),
        factory: SubjectEducatorFactory = Depends(get_authenticated_factory(SubjectEducatorFactory))
    ):
    return factory.get_all_subject_educators(filters)


@router.get("/{subject_educator_id}/audit", response_model=SubjectEducatorAudit)
def get_subject_educator_audit(
        subject_educator_id: UUID,
        factory: SubjectEducatorFactory = Depends(get_authenticated_factory(SubjectEducatorFactory))
    ):
    return factory.get_subject_educator(subject_educator_id)


@router.get("/{subject_educator_id}", response_model=SubjectEducatorResponse)
def get_subject_educator(
        subject_educator_id: UUID,
        factory: SubjectEducatorFactory = Depends(get_authenticated_factory(SubjectEducatorFactory))
    ):
    return factory.get_subject_educator(subject_educator_id)


@router.patch("/{subject_educator_id}",  status_code=204)
def archive_subject_educator(
        subject_educator_id: UUID,
        reason:ArchiveRequest,
        factory: SubjectEducatorFactory = Depends(get_authenticated_factory(SubjectEducatorFactory))
    ):
    return factory.archive_subject_educator(subject_educator_id, reason.reason)


@router.delete("/{subject_educator_id}", status_code=204)
def delete_subject_educator(
        subject_educator_id: UUID,
        factory: SubjectEducatorFactory = Depends(get_authenticated_factory(SubjectEducatorFactory))
    ):
    return factory.delete_subject_educator(subject_educator_id)










