from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from V2.app.core.staff_management.factories.department import StaffDepartmentFactory
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory
from V2.app.core.staff_management.schemas.department import(
   StaffDepartmentResponse, DepartmentFilterParams, StaffDepartmentAudit
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer

token_service = TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/archived", response_model=List[StaffDepartmentResponse])
def get_archived_staff_departments(
        filters: DepartmentFilterParams = Depends(),
        factory: StaffDepartmentFactory = Depends(get_authenticated_factory(StaffDepartmentFactory))
    ):
    """Get all archived departments."""
    return factory.get_all_archived_departments(filters)


@router.get("/archived/{department_id}/audit", response_model=StaffDepartmentAudit)
def get_archived_staff_department_audit(
        department_id: UUID,
        factory: StaffDepartmentFactory = Depends(get_authenticated_factory(StaffDepartmentFactory))
    ):
    """Get an archived department audit by ID."""
    return factory.get_archived_department(department_id)


@router.get("/archived/{department_id}", response_model=StaffDepartmentResponse)
def get_archived_department(
        department_id: UUID,
        factory: StaffDepartmentFactory = Depends(get_authenticated_factory(StaffDepartmentFactory))
    ):
    """Get an archived department by ID."""
    return factory.get_archived_department(department_id)


@router.post("/archived/{department_id}/restore", response_model=StaffDepartmentResponse)
def restore_department(
        department_id: UUID,
        factory: StaffDepartmentFactory = Depends(get_authenticated_factory(StaffDepartmentFactory))
    ):
    """Restore an archived department."""
    return factory.restore_department(department_id)


@router.delete("/archived/{department_id}", status_code=204)
def delete_archived_department(
        department_id: UUID,
        factory: StaffDepartmentFactory = Depends(get_authenticated_factory(StaffDepartmentFactory))
    ):
    """Permanently delete an archived department."""
    return factory.delete_archived_department(department_id)










