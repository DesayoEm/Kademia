
from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from V2.app.core.curriculum.crud.subject_educator import SubjectEducatorCrud
from V2.app.core.curriculum.schemas.subject_educator import (
   SubjectEducatorResponse, SubjectEducatorFilterParams
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[SubjectEducatorResponse])
def get_archived_subject_educators(
        filters: SubjectEducatorFilterParams = Depends(),
        crud: SubjectEducatorCrud = Depends(get_authenticated_crud(SubjectEducatorCrud))
    ):
    return crud.get_all_archived_subject_educators(filters)


@router.get("/{subject_educator_id}", response_model=SubjectEducatorResponse)
def get_archived_subject_educator(
        subject_educator_id: UUID,
        crud: SubjectEducatorCrud = Depends(get_authenticated_crud(SubjectEducatorCrud))
    ):
    return crud.get_archived_subject_educator(subject_educator_id)


@router.patch("/{subject_educator_id}", response_model=SubjectEducatorResponse)
def restore_subject_educator(
        subject_educator_id: UUID,
        crud: SubjectEducatorCrud = Depends(get_authenticated_crud(SubjectEducatorCrud))
    ):
    return crud.restore_subject_educator(subject_educator_id)


@router.delete("/{subject_educator_id}", status_code=204)
def delete_archived_subject_educator(
        subject_educator_id: UUID,
        crud: SubjectEducatorCrud = Depends(get_authenticated_crud(SubjectEducatorCrud))
    ):
    return crud.delete_archived_subject_educator(subject_educator_id)




