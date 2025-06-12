from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from V2.app.core.transfer.crud.department_transfer import StudentDepartmentTransferCrud
from V2.app.core.transfer.schemas.department_transfer import (
    StudentDepartmentTransferResponse,
    DepartmentTransferFilterParams
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[StudentDepartmentTransferResponse])
def get_archived_transfers(
        filters: DepartmentTransferFilterParams = Depends(), 
        crud:  StudentDepartmentTransferCrud = Depends(get_authenticated_crud(StudentDepartmentTransferCrud))
    ):
    return crud.get_all_archived_transfers(filters)


@router.get("/{transfer_id}", response_model=StudentDepartmentTransferResponse)
def get_archived_transfer(
        transfer_id: UUID,
        crud:  StudentDepartmentTransferCrud = Depends(get_authenticated_crud(StudentDepartmentTransferCrud))
    ):
    return crud.get_archived_transfer(transfer_id)


@router.patch("/{transfer_id}", response_model=StudentDepartmentTransferResponse)
def restore_transfer(
        transfer_id: UUID, 
        crud:  StudentDepartmentTransferCrud = Depends(get_authenticated_crud(StudentDepartmentTransferCrud))
    ):
    return crud.restore_transfer(transfer_id)


@router.delete("/{transfer_id}", status_code=204)
def delete_archived_transfer(
        transfer_id: UUID, 
        crud:  StudentDepartmentTransferCrud = Depends(get_authenticated_crud(StudentDepartmentTransferCrud))
    ):
    return crud.delete_archived_transfer(transfer_id)
