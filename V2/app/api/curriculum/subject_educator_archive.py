from V2.app.core.curriculum.factories.subject_educator import SubjectEducatorFactory


from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from V2.app.core.curriculum.schemas.subject_educator import (
    SubjectEducatorResponse, SubjectEducatorFilterParams, SubjectEducatorAudit
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[SubjectEducatorResponse])
def get_archived_subject_educators(
        filters: SubjectEducatorFilterParams = Depends(),
        factory: SubjectEducatorFactory = Depends(get_authenticated_factory(SubjectEducatorFactory))
    ):
    return factory.get_all_archived_subject_educators(filters)


@router.get("/{subject_educator_id}/audit", response_model=SubjectEducatorAudit)
def get_archived_subject_educator_audit(
        subject_educator_id: UUID,
        factory: SubjectEducatorFactory = Depends(get_authenticated_factory(SubjectEducatorFactory))
    ):
    return factory.get_archived_subject_educator(subject_educator_id)


@router.get("/{subject_educator_id}", response_model=SubjectEducatorResponse)
def get_archived_subject_educator(
        subject_educator_id: UUID,
        factory: SubjectEducatorFactory = Depends(get_authenticated_factory(SubjectEducatorFactory))
    ):
    return factory.get_archived_subject_educator(subject_educator_id)


@router.patch("/{subject_educator_id}", response_model=SubjectEducatorResponse)
def restore_subject_educator(
        subject_educator_id: UUID,
        factory: SubjectEducatorFactory = Depends(get_authenticated_factory(SubjectEducatorFactory))
    ):
    return factory.restore_subject_educator(subject_educator_id)


@router.delete("/{subject_educator_id}", status_code=204)
def delete_archived_subject_educator(
        subject_educator_id: UUID,
        factory: SubjectEducatorFactory = Depends(get_authenticated_factory(SubjectEducatorFactory))
    ):
    return factory.delete_archived_subject_educator(subject_educator_id)




