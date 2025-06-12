from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List
from V2.app.core.transfer.crud.department_transfer import StudentDepartmentTransferCrud
from V2.app.core.transfer.schemas.department_transfer import (
    StudentDepartmentTransferCreate,
    StudentDepartmentTransferResponse,
    DepartmentTransferFilterParams
)
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("/students/{student_id}", response_model=StudentDepartmentTransferResponse, status_code=201)
def create_transfer(
        student_id: UUID, 
        payload: StudentDepartmentTransferCreate, 
        crud: StudentDepartmentTransferCrud = Depends(get_authenticated_crud(StudentDepartmentTransferCrud))
    ):
    return crud.create_transfer(student_id, payload)


@router.get("/", response_model=List[StudentDepartmentTransferResponse])
def get_transfers(
        filters: DepartmentTransferFilterParams = Depends(), 
        crud: StudentDepartmentTransferCrud = Depends(get_authenticated_crud(StudentDepartmentTransferCrud))
    ):
    return crud.get_all_transfers(filters)


@router.get("/{transfer_id}", response_model=StudentDepartmentTransferResponse)
def get_transfer(
        transfer_id: UUID, 
        crud: StudentDepartmentTransferCrud = Depends(get_authenticated_crud(StudentDepartmentTransferCrud))
    ):
    return crud.get_transfer(transfer_id)



@router.patch("/{transfer_id}", status_code=204)
def archive_transfer(
        transfer_id: UUID, 
        reason: ArchiveRequest, 
        crud: StudentDepartmentTransferCrud = Depends(get_authenticated_crud(StudentDepartmentTransferCrud))
    ):
    return crud.archive_transfer(transfer_id, reason.reason)


@router.delete("/{transfer_id}", status_code=204)
def delete_transfer(
        transfer_id: UUID, 
        crud: StudentDepartmentTransferCrud = Depends(get_authenticated_crud(StudentDepartmentTransferCrud))
    ):
    return crud.delete_transfer(transfer_id)
