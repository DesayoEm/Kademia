
from fastapi import Depends, APIRouter
from uuid import UUID
from typing import List
from V2.app.core.assessment.schemas.total_grade import TotalGradeFilterParams, TotalGradeResponse

from V2.app.core.assessment.crud.total_grade import TotalGradeCrud
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/{student_subject_id}", response_model= TotalGradeResponse, status_code=201)
def generate_total_grade(
        student_subject_id: UUID,
        crud: TotalGradeCrud = Depends(get_authenticated_crud(TotalGradeCrud))
    ):
    return crud.create_total_grade(student_subject_id)


@router.get("/", response_model=List[TotalGradeResponse])
def get_total_grades(
        filters: TotalGradeFilterParams = Depends(),
        crud: TotalGradeCrud = Depends(get_authenticated_crud(TotalGradeCrud))
    ):
    return crud.get_all_total_grades(filters)


@router.get("/{grade_id}", response_model=TotalGradeResponse)
def get_total_grade(
        grade_id: UUID,
        crud: TotalGradeCrud = Depends(get_authenticated_crud(TotalGradeCrud))
    ):
    return crud.get_total_grade(grade_id)


@router.patch("/{grade_id}", response_model=TotalGradeResponse)
def restore_total_grade(
        grade_id: UUID,
        crud: TotalGradeCrud = Depends(get_authenticated_crud(TotalGradeCrud))
    ):
    return crud.restore_total_grade(grade_id)


@router.delete("/{grade_id}", status_code=204)
def delete_total_grade(
        grade_id: UUID,
        crud: TotalGradeCrud = Depends(get_authenticated_crud(TotalGradeCrud))
    ):
    return crud.delete_total_grade(grade_id)




