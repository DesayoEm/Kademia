
from fastapi import Depends, APIRouter
from uuid import UUID
from typing import List
from V2.app.core.assessment.schemas.grade import GradeFilterParams, GradeResponse, GradeAudit
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.assessment.factories.grade import GradeFactory
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[GradeResponse])
def get_archived_grades(
        filters: GradeFilterParams = Depends(),
        factory: GradeFactory = Depends(get_authenticated_factory(GradeFactory))
    ):
    return factory.get_all_archived_grades(filters)



@router.get("/{grade_id}/audit", response_model=GradeAudit)
def get_archived_grade_audit(
        grade_id: UUID,
        factory: GradeFactory = Depends(get_authenticated_factory(GradeFactory))
):
    return factory.get_archived_grade(grade_id)


@router.get("/{grade_id}", response_model=GradeResponse)
def get_archived_grade(
        grade_id: UUID,
        factory: GradeFactory = Depends(get_authenticated_factory(GradeFactory))
):
    return factory.get_archived_grade(grade_id)


@router.patch("/{grade_id}", response_model=GradeResponse)
def restore_grade(
        grade_id: UUID,
        factory: GradeFactory = Depends(get_authenticated_factory(GradeFactory))
    ):
    return factory.restore_grade(grade_id)


@router.delete("/{grade_id}", status_code=204)
def delete_archived_grade(
        grade_id: UUID,
        factory: GradeFactory = Depends(get_authenticated_factory(GradeFactory))
    ):
    return factory.delete_archived_grade(grade_id)




