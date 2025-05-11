
from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from V2.app.core.curriculum.crud.student_subject import StudentSubjectCrud
from V2.app.core.curriculum.schemas.student_subject import (
   StudentSubjectResponse, StudentSubjectFilterParams
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[StudentSubjectResponse])
def get_archived_student_subjects(
        filters: StudentSubjectFilterParams = Depends(),
        crud: StudentSubjectCrud = Depends(get_authenticated_crud(StudentSubjectCrud))
    ):
    return crud.get_all_archived_student_subjects(filters)


@router.get("/{student_subject_id}", response_model=StudentSubjectResponse)
def get_archived_student_subject(
        student_subject_id: UUID,
        crud: StudentSubjectCrud = Depends(get_authenticated_crud(StudentSubjectCrud))
    ):
    return crud.get_archived_student_subject(student_subject_id)


@router.patch("/{student_subject_id}", response_model=StudentSubjectResponse)
def restore_student_subject(
        student_subject_id: UUID,
        crud: StudentSubjectCrud = Depends(get_authenticated_crud(StudentSubjectCrud))
    ):
    return crud.restore_student_subject(student_subject_id)


@router.delete("/{student_subject_id}", status_code=204)
def delete_archived_student_subject(
        student_subject_id: UUID,
        crud: StudentSubjectCrud = Depends(get_authenticated_crud(StudentSubjectCrud))
    ):
    return crud.delete_archived_student_subject(student_subject_id)




