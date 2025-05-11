
from uuid import UUID
from typing import List
from V2.app.core.identity.schemas.student import StudentResponse, StudentFilterParams
from fastapi import Depends, APIRouter
from V2.app.core.identity.crud.student import StudentCrud
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[StudentResponse])
def get_archived_students(
        filters: StudentFilterParams = Depends(),
        crud: StudentCrud = Depends(get_authenticated_crud(StudentCrud))
    ):
    return crud.get_all_archived_student(filters)


@router.get("/{student_id}", response_model=StudentResponse)
def get_archived_student(
        student_id: UUID,
        crud: StudentCrud = Depends(get_authenticated_crud(StudentCrud))
    ):
    return crud.get_archived_student(student_id)


@router.patch("/{student_id}", response_model=StudentResponse)
def restore_student(
        student_id: UUID,
        crud: StudentCrud = Depends(get_authenticated_crud(StudentCrud))
):
    return crud.restore_student(student_id)


@router.delete("/{student_id}", status_code=204)
def delete_archived_student(
        student_id: UUID,
        crud: StudentCrud = Depends(get_authenticated_crud(StudentCrud))
):
    return crud.delete_archived_student(student_id)











