from typing import List
from uuid import UUID
from fastapi import Depends, APIRouter

from app.core.curriculum.factories.subject import SubjectFactory

from app.core.curriculum.schemas.subject import SubjectFilterParams, SubjectResponse, SubjectAudit
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory



token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[SubjectResponse])
def get_archived_subjects(
        filters: SubjectFilterParams = Depends(),
        crud: SubjectFactory = Depends(get_authenticated_factory(SubjectFactory))
    ):
    return crud.get_all_archived_subjects(filters)


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_archived_subject(
        subject_id: UUID,
        crud: SubjectFactory = Depends(get_authenticated_factory(SubjectFactory))
    ):
    return crud.get_archived_subject(subject_id)


@router.get("/{subject_id}/audit", response_model=SubjectAudit)
def get_archived_subject_audit(
        subject_id: UUID,
        crud: SubjectFactory = Depends(get_authenticated_factory(SubjectFactory))
    ):
    return crud.get_archived_subject(subject_id)


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_archived_subject(
        subject_id: UUID,
        crud: SubjectFactory = Depends(get_authenticated_factory(SubjectFactory))
    ):
    return crud.get_archived_subject(subject_id)


@router.patch("/{subject_id}", response_model=SubjectResponse)
def restore_subject(
        subject_id: UUID,
        crud: SubjectFactory = Depends(get_authenticated_factory(SubjectFactory))
    ):
    return crud.restore_subject(subject_id)


@router.delete("/{subject_id}", status_code=204)
def delete_archived_subject(
        subject_id: UUID,
        crud: SubjectFactory = Depends(get_authenticated_factory(SubjectFactory))
    ):
    return crud.delete_archived_subject(subject_id)




