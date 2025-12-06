from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from app.core.transfer.factories.transfer import TransferFactory

from app.core.transfer.schemas.department_transfer import (
    DepartmentTransferCreate,
    DepartmentTransferResponse,
    DepartmentTransferFilterParams,
    DepartmentTransferUpdate,
    DepartmentTransferDecision,
)
from app.core.shared.schemas.shared_models import ArchiveRequest
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import (
    get_authenticated_service,
    get_authenticated_factory,
)
from app.core.transfer.services.transfer_service import TransferService

token_service = TokenService()
access = AccessTokenBearer()
router = APIRouter()


# Archive
@router.get("/archive/transfers", response_model=List[DepartmentTransferResponse])
def get_archived_transfers(
    filters: DepartmentTransferFilterParams = Depends(),
    factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory)),
):
    return factory.get_all_archived_transfers(filters)


@router.get(
    "/archive/transfers/{transfer_id}", response_model=DepartmentTransferResponse
)
def get_archived_transfer(
    transfer_id: UUID,
    factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory)),
):
    return factory.get_archived_transfer(transfer_id)


@router.patch(
    "/archive/transfers/{transfer_id}", response_model=DepartmentTransferResponse
)
def restore_transfer(
    transfer_id: UUID,
    factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory)),
):
    return factory.restore_transfer(transfer_id)


@router.delete("/archive/transfers/{transfer_id}", status_code=204)
def delete_archived_transfer(
    transfer_id: UUID,
    factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory)),
):
    return factory.delete_archived_transfer(transfer_id)


@router.post(
    "/students/{student_id}/transfer",
    response_model=DepartmentTransferResponse,
    status_code=201,
)
def create_transfer(
    student_id: UUID,
    payload: DepartmentTransferCreate,
    factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory)),
):
    return factory.create_transfer(student_id, payload)


@router.get("/transfers/", response_model=List[DepartmentTransferResponse])
def get_transfers(
    filters: DepartmentTransferFilterParams = Depends(),
    factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory)),
):
    return factory.get_all_transfers(filters)


@router.get("/transfers/{transfer_id}", response_model=DepartmentTransferResponse)
def get_transfer(
    transfer_id: UUID,
    factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory)),
):
    return factory.get_transfer(transfer_id)


@router.patch(
    "/transfers/{transfer_id}/action", response_model=DepartmentTransferResponse
)
def action_transfer(
    transfer_id: UUID,
    payload: DepartmentTransferDecision,
    service: TransferService = Depends(get_authenticated_service(TransferService)),
):
    payload = payload.model_dump(exclude_unset=True)
    return service.action_transfer_record(transfer_id, payload)


@router.patch("/transfers/{transfer_id}", response_model=DepartmentTransferResponse)
def update_transfer(
    transfer_id: UUID,
    payload: DepartmentTransferUpdate,
    factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory)),
):
    payload = payload.model_dump(exclude_unset=True)
    return factory.update_transfer(transfer_id, payload)


@router.patch("/transfers/{transfer_id}", status_code=204)
def archive_transfer(
    transfer_id: UUID,
    reason: ArchiveRequest,
    factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory)),
):
    return factory.archive_transfer(transfer_id, reason.reason)


@router.delete("/transfers/{transfer_id}", status_code=204)
def delete_transfer(
    transfer_id: UUID,
    factory: TransferFactory = Depends(get_authenticated_factory(TransferFactory)),
):
    return factory.delete_transfer(transfer_id)
