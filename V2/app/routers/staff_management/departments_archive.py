from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.infra.db.session_manager import get_db
from V2.app.core.staff_management.crud.department import StaffDepartmentCrud
from V2.app.core.staff_management.schemas.department import StaffDepartmentResponse, DepartmentFilterParams
from fastapi import Depends, APIRouter
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud, get_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[StaffDepartmentResponse])
def get_archived_staff_departments(
        filters: DepartmentFilterParams = Depends(),
        crud: StaffDepartmentCrud = Depends(get_authenticated_crud(StaffDepartmentCrud))
):
    return crud.get_all_archived_departments(filters)


@router.get("/{department_id}", response_model=StaffDepartmentResponse)
def get_archived_staff_department(
        department_id: UUID,
        crud: StaffDepartmentCrud = Depends(get_authenticated_crud(StaffDepartmentCrud))
    ):
    return crud.get_archived_department(department_id)


@router.patch("/{department_id}", response_model=StaffDepartmentResponse)
def restore_department(
        department_id: UUID,
        crud: StaffDepartmentCrud = Depends(get_authenticated_crud(StaffDepartmentCrud))
):
    return crud.restore_department(department_id)


@router.delete("/{department_id}", status_code=204)
def delete_archived_department(
        department_id: UUID,
        crud: StaffDepartmentCrud = Depends(get_authenticated_crud(StaffDepartmentCrud))
    ):
    return crud.delete_archived_department(department_id)










