from uuid import UUID
from typing import List
from app.core.curriculum.factories.academic_level_subject import AcademicLevelSubjectFactory
from fastapi import Depends, APIRouter
from app.core.curriculum.schemas.academic_level_subject import(
    AcademicLevelSubjectFilterParams, AcademicLevelSubjectResponse
)
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[AcademicLevelSubjectResponse])
def get_archived_level_subjects(
        filters: AcademicLevelSubjectFilterParams = Depends(),
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.get_all_archived_academic_level_subjects(filters)


@router.get("/{level_subject_id}", response_model=AcademicLevelSubjectResponse)
def get_archived_level_subject(
        level_subject_id: UUID,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.get_archived_academic_level_subject(level_subject_id)


@router.patch("/{level_subject_id}", response_model=AcademicLevelSubjectResponse)
def restore_level_subject(
        level_subject_id: UUID,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.restore_academic_level_subject(level_subject_id)


@router.delete("/{level_subject_id}", status_code=204)
def delete_archived_level_subject(
        level_subject_id: UUID,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.delete_archived_academic_level_subject(level_subject_id)




