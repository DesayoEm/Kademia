from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from app.core.transfer.factories.transfer import TransferFactory

from app.core.transfer.schemas.department_transfer import (
    DepartmentTransferCreate,
    DepartmentTransferResponse,
    DepartmentTransferFilterParams,
    DepartmentTransferUpdate, DepartmentTransferDecision
)
from app.core.shared.schemas.shared_models import ArchiveRequest
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_service, get_authenticated_factory
from app.core.transfer.services.transfer_service import TransferService

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("/students/{student_id}", response_model=DepartmentTransferResponse, status_code=201)
def create_transfer(
        student_id: UUID, 
        payload: DepartmentTransferCreate,
        factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory))
    ):
    return factory.create_transfer(student_id, payload)


@router.get("/", response_model=List[DepartmentTransferResponse])
def get_transfers(
        filters: DepartmentTransferFilterParams = Depends(), 
        factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory))
    ):
    return factory.get_all_transfers(filters)


@router.get("/{transfer_id}", response_model=DepartmentTransferResponse)
def get_transfer(
        transfer_id: UUID, 
        factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory))
    ):
    return factory.get_transfer(transfer_id)

@router.patch("/{student_id}/transfers/action", response_model=DepartmentTransferResponse)
def action_transfer(
        transfer_id: UUID,
        payload: DepartmentTransferDecision,
        service: TransferService = Depends(get_authenticated_service(TransferService))
    ):
    payload = payload.model_dump(exclude_unset=True)
    return service.action_transfer_record(transfer_id, payload)


@router.patch("/{student_id}/transfers", response_model=DepartmentTransferResponse)
def update_transfer(
        transfer_id: UUID,
        payload: DepartmentTransferUpdate,
        factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory))
    ):
    payload = payload.model_dump(exclude_unset=True)
    return factory.update_transfer(transfer_id, payload)


@router.patch("/{student_id}/{transfer_id}", status_code=204)
def archive_transfer(
        transfer_id: UUID, 
        reason: ArchiveRequest, 
        factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory))
    ):
    return factory.archive_transfer(transfer_id, reason.reason)


@router.delete("/{transfer_id}", status_code=204)
def delete_transfer(
        transfer_id: UUID, 
        factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory))
    ):
    return factory.delete_transfer(transfer_id)



#Archive
@router.get("/archived", response_model=List[DepartmentTransferResponse])
def get_archived_transfers(
        filters: DepartmentTransferFilterParams = Depends(), 
        factory:  TransferFactory = Depends(get_authenticated_factory(TransferFactory))
    ):
    return factory.get_all_archived_transfers(filters)


@router.get("archived/{transfer_id}", response_model=DepartmentTransferResponse)
def get_archived_transfer(
        transfer_id: UUID,
        factory:  TransferFactory = Depends(get_authenticated_factory(TransferFactory))
    ):
    return factory.get_archived_transfer(transfer_id)


@router.patch("archived/{transfer_id}", response_model=DepartmentTransferResponse)
def restore_transfer(
        transfer_id: UUID, 
        factory:  TransferFactory = Depends(get_authenticated_factory(TransferFactory))
    ):
    return factory.restore_transfer(transfer_id)


@router.delete("archived/{transfer_id}", status_code=204)
def delete_archived_transfer(
        transfer_id: UUID, 
        factory:  TransferFactory = Depends(get_authenticated_factory(TransferFactory))
    ):
    return factory.delete_archived_transfer(transfer_id)

