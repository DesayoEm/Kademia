
from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter

from V2.app.core.academic_structure.schemas.department import (
    DepartmentFilterParams, DepartmentResponse, DepartmentAudit
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.academic_structure.factories.department import StudentDepartmentFactory
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[DepartmentResponse])
def get_archived_departments(
        filters: DepartmentFilterParams = Depends(),
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.get_all_archived_departments(filters)


@router.get("/{department_id}/audit", response_model=DepartmentAudit)
def get_archived_department_audit(
        department_id: UUID,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.get_archived_department(department_id)

@router.get("/{department_id}", response_model=DepartmentResponse)
def get_archived_department(
        department_id: UUID,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.get_archived_department(department_id)


@router.patch("/{department_id}", response_model=DepartmentResponse)
def restore_department(
        department_id: UUID,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.restore_department(department_id)


@router.delete("/{department_id}", status_code=204)
def delete_archived_department(
        department_id: UUID,
        factory: StudentDepartmentFactory = Depends(get_authenticated_factory(StudentDepartmentFactory))
    ):
    return factory.delete_archived_department(department_id)




