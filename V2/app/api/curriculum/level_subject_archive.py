
from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from V2.app.core.curriculum.crud.academic_level_subject import AcademicLevelSubjectCrud
from V2.app.core.curriculum.schemas.academic_level_subject import (
   AcademicLevelSubjectResponse, AcademicLevelSubjectFilterParams
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[AcademicLevelSubjectResponse])
def get_archived_level_subjects(
        filters: AcademicLevelSubjectFilterParams = Depends(),
        crud: AcademicLevelSubjectCrud = Depends(get_authenticated_crud(AcademicLevelSubjectCrud))
    ):
    return crud.get_all_archived_level_subjects(filters)


@router.get("/{level_subject_id}", response_model=AcademicLevelSubjectResponse)
def get_archived_level_subject(
        level_subject_id: UUID,
        crud: AcademicLevelSubjectCrud = Depends(get_authenticated_crud(AcademicLevelSubjectCrud))
    ):
    return crud.get_archived_level_subject(level_subject_id)


@router.patch("/{level_subject_id}", response_model=AcademicLevelSubjectResponse)
def restore_level_subject(
        level_subject_id: UUID,
        crud: AcademicLevelSubjectCrud = Depends(get_authenticated_crud(AcademicLevelSubjectCrud))
    ):
    return crud.restore_level_subject(level_subject_id)


@router.delete("/{level_subject_id}", status_code=204)
def delete_archived_level_subject(
        level_subject_id: UUID,
        crud: AcademicLevelSubjectCrud = Depends(get_authenticated_crud(AcademicLevelSubjectCrud))
    ):
    return crud.delete_archived_level_subject(level_subject_id)




