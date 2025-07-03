
from fastapi import Depends, APIRouter
from uuid import UUID
from typing import List

from V2.app.core.assessment.factories.total_grade import TotalGradeFactory
from V2.app.core.assessment.schemas.total_grade import TotalGradeFilterParams, TotalGradeResponse, TotalGradeAudit

from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[TotalGradeResponse])
def get_archived_total_grades(
        filters: TotalGradeFilterParams = Depends(),
        factory: TotalGradeFactory = Depends(get_authenticated_factory(TotalGradeFactory))
    ):
    return factory.get_all_archived_total_grades(filters)


@router.get("/{total_grade_id}/audit", response_model=TotalGradeAudit)
def get_archived_total_grade_audit(
        total_grade_id: UUID,
        factory: TotalGradeFactory = Depends(get_authenticated_factory(TotalGradeFactory))
    ):
    return factory.get_archived_total_grade(total_grade_id)


@router.get("/{total_grade_id}", response_model=TotalGradeResponse)
def get_archived_total_grade(
        total_grade_id: UUID,
        factory: TotalGradeFactory = Depends(get_authenticated_factory(TotalGradeFactory))
    ):
    return factory.get_archived_total_grade(total_grade_id)


@router.patch("/{total_grade_id}", response_model=TotalGradeResponse)
def restore_total_grade(
        total_grade_id: UUID,
        factory: TotalGradeFactory = Depends(get_authenticated_factory(TotalGradeFactory))
    ):
    return factory.restore_total_grade(total_grade_id)


@router.delete("/{total_grade_id}", status_code=204)
def delete_archived_total_grade(
        total_grade_id: UUID,
        factory: TotalGradeFactory = Depends(get_authenticated_factory(TotalGradeFactory))
    ):
    return factory.delete_archived_total_grade(total_grade_id)




