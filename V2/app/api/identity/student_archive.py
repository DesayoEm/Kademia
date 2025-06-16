
from uuid import UUID
from typing import List
from V2.app.core.identity.schemas.student import StudentResponse, StudentFilterParams, StudentAudit
from fastapi import Depends, APIRouter
from V2.app.core.identity.factories.student import StudentFactory
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[StudentResponse])
def get_archived_students(
        filters: StudentFilterParams = Depends(),
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
    return factory.get_all_archived_students(filters)


@router.get("/{student_id}/audit", response_model=StudentAudit)
def get_archived_student_audit(
        student_id: UUID,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
    return factory.get_archived_student(student_id)


@router.get("/{student_id}", response_model=StudentResponse)
def get_archived_student(
        student_id: UUID,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
    return factory.get_archived_student(student_id)


@router.patch("/{student_id}", response_model=StudentResponse)
def restore_student(
        student_id: UUID,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
):
    return factory.restore_student(student_id)


@router.delete("/{student_id}", status_code=204)
def delete_archived_student(
        student_id: UUID,
        factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
):
    return factory.delete_archived_student(student_id)











