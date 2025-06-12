
from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from V2.app.core.academic_structure.crud.departments import DepartmentCrud
from V2.app.core.academic_structure.schemas.department import(
     DepartmentFilterParams, DepartmentResponse
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[DepartmentResponse])
def get_archived_departments(
        filters: DepartmentFilterParams = Depends(),
        crud: DepartmentCrud = Depends(get_authenticated_crud(DepartmentCrud))
    ):
    return crud.get_all_archived_departments(filters)


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_archived_department(
        department_id: UUID,
        crud: DepartmentCrud = Depends(get_authenticated_crud(DepartmentCrud))
    ):
    return crud.get_archived_department(department_id)


@router.patch("/{department_id}", response_model=DepartmentResponse)
def restore_department(
        department_id: UUID,
        crud: DepartmentCrud = Depends(get_authenticated_crud(DepartmentCrud))
    ):
    return crud.restore_department(department_id)


@router.delete("/{department_id}", status_code=204)
def delete_archived_department(
        department_id: UUID,
        crud: DepartmentCrud = Depends(get_authenticated_crud(DepartmentCrud))
    ):
    return crud.delete_archived_department(department_id)




