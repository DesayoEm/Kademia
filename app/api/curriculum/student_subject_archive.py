
from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from app.core.curriculum.factories.student_subject import StudentSubjectFactory
from app.core.curriculum.schemas.student_subject import (
    StudentSubjectResponse, StudentSubjectFilterParams, StudentSubjectAudit
)
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[StudentSubjectResponse])
def get_archived_student_subjects(
        filters: StudentSubjectFilterParams = Depends(),
        factory: StudentSubjectFactory = Depends(get_authenticated_factory(StudentSubjectFactory))
    ):
    return factory.get_all_archived_student_subjects(filters)


@router.get("/{student_subject_id}/audit", response_model=StudentSubjectAudit)
def get_archived_student_subject_audit(
        student_subject_id: UUID,
        factory: StudentSubjectFactory = Depends(get_authenticated_factory(StudentSubjectFactory))
    ):
    return factory.get_archived_student_subject(student_subject_id)


@router.get("/{student_subject_id}", response_model=StudentSubjectResponse)
def get_archived_student_subject(
        student_subject_id: UUID,
        factory: StudentSubjectFactory = Depends(get_authenticated_factory(StudentSubjectFactory))
    ):
    return factory.get_archived_student_subject(student_subject_id)


@router.patch("/{student_subject_id}", response_model=StudentSubjectResponse)
def restore_student_subject(
        student_subject_id: UUID,
        factory: StudentSubjectFactory = Depends(get_authenticated_factory(StudentSubjectFactory))
    ):
    return factory.restore_student_subject(student_subject_id)


@router.delete("/{student_subject_id}", status_code=204)
def delete_archived_student_subject(
        student_subject_id: UUID,
        factory: StudentSubjectFactory = Depends(get_authenticated_factory(StudentSubjectFactory))
    ):
    return factory.delete_archived_student_subject(student_subject_id)




