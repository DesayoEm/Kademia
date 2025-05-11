from typing import List
from uuid import UUID
from fastapi import Depends, APIRouter

from V2.app.core.curriculum.crud.subject import SubjectCrud
from V2.app.core.curriculum.schemas.subject import SubjectFilterParams, SubjectResponse
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[SubjectResponse])
def get_archived_subjects(
        filters: SubjectFilterParams = Depends(),
        crud: SubjectCrud = Depends(get_authenticated_crud(SubjectCrud))
    ):
    return crud.get_all_archived_subjects(filters)


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_archived_subject(
        subject_id: UUID,
        crud: SubjectCrud = Depends(get_authenticated_crud(SubjectCrud))
    ):
    return crud.get_archived_subject(subject_id)


@router.patch("/{subject_id}", response_model=SubjectResponse)
def restore_subject(
        subject_id: UUID,
        crud: SubjectCrud = Depends(get_authenticated_crud(SubjectCrud))
    ):
    return crud.restore_subject(subject_id)


@router.delete("/{subject_id}", status_code=204)
def delete_archived_subject(
        subject_id: UUID,
        crud: SubjectCrud = Depends(get_authenticated_crud(SubjectCrud))
    ):
    return crud.delete_archived_subject(subject_id)




