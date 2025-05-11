
from uuid import UUID
from typing import List
from V2.app.core.identity.schemas.staff import StaffResponse, StaffFilterParams
from fastapi import Depends, APIRouter

from V2.app.core.identity.crud.staff import StaffCrud
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[StaffResponse])
def get_archived_staff(
        filters: StaffFilterParams = Depends(),
        crud: StaffCrud = Depends(get_authenticated_crud(StaffCrud))
    ):
    return crud.get_all_archived_staff(filters)


@router.get("/{staff_id}", response_model=StaffResponse)
def get_archived_staff(
        staff_id: UUID,
        crud: StaffCrud = Depends(get_authenticated_crud(StaffCrud))
    ):
    return crud.get_archived_staff(staff_id)


@router.patch("/{staff_id}", response_model=StaffResponse)
def restore_staff(
        staff_id: UUID,
        crud: StaffCrud = Depends(get_authenticated_crud(StaffCrud))
    ):
    return crud.restore_staff(staff_id)


@router.delete("/{staff_id}", status_code=204)
def delete_archived_staff(
        staff_id: UUID,
        crud: StaffCrud = Depends(get_authenticated_crud(StaffCrud))
    ):
    return crud.delete_archived_staff(staff_id)











