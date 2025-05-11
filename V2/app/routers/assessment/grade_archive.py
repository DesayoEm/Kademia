
from fastapi import Depends, APIRouter
from uuid import UUID
from typing import List
from V2.app.core.assessment.schemas.grade import GradeFilterParams, GradeResponse
from V2.app.core.assessment.crud.grade import GradeCrud
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[GradeResponse])
def get_archived_grades(
        filters: GradeFilterParams = Depends(),
        crud: GradeCrud = Depends(get_authenticated_crud(GradeCrud))
    ):
    return crud.get_all_archived_grades(filters)


@router.get("/{grade_id}", response_model=GradeResponse)
def get_archived_grade(
        grade_id: UUID,
        crud: GradeCrud = Depends(get_authenticated_crud(GradeCrud))
):
    return crud.get_archived_grade(grade_id)


@router.patch("/{grade_id}", response_model=GradeResponse)
def restore_grade(
        grade_id: UUID,crud:
        GradeCrud = Depends(get_authenticated_crud(GradeCrud))
    ):
    return crud.restore_grade(grade_id)


@router.delete("/{grade_id}", status_code=204)
def delete_archived_grade(
        grade_id: UUID, crud:
        GradeCrud = Depends(get_authenticated_crud(GradeCrud))
    ):
    return crud.delete_archived_grade(grade_id)




