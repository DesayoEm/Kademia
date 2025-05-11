
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


@router.get("/", response_model=List[TotalGradeResponse])
def get_archived_total_grades(
        filters: TotalGradeFilterParams = Depends(),
        crud: TotalGradeCrud = Depends(get_authenticated_crud(TotalGradeCrud))
    ):
    return crud.get_all_archived_total_grades(filters)


@router.get("/{total_grade_id}", response_model=TotalGradeResponse)
def get_archived_total_grade(
        total_grade_id: UUID,
        crud: TotalGradeCrud = Depends(get_authenticated_crud(TotalGradeCrud))
    ):
    return crud.get_archived_total_grade(total_grade_id)


@router.patch("/{total_grade_id}", response_model=TotalGradeResponse)
def restore_total_grade(
        total_grade_id: UUID,
        crud: TotalGradeCrud = Depends(get_authenticated_crud(TotalGradeCrud))
    ):
    return crud.restore_total_grade(total_grade_id)


@router.delete("/{total_grade_id}", status_code=204)
def delete_archived_total_grade(
        total_grade_id: UUID,
        crud: TotalGradeCrud = Depends(get_authenticated_crud(TotalGradeCrud))
    ):
    return crud.delete_archived_total_grade(total_grade_id)




