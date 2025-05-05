from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.transfer.factories.class_transfer import ClassTransferFactory
from V2.app.core.transfer.models.transfer import ClassTransfer
from V2.app.core.transfer.schemas.class_transfer import (
    StudentClassTransferCreate,
    StudentClassTransferUpdate,
    StudentClassTransferResponse,
    ClassTransferFilterParams
)
from V2.app.core.shared.schemas.enums import ArchiveReason


class ClassTransferCrud:
    """CRUD operations for student class transfers."""

    def __init__(self, session: Session):
        self.session = session
        self.factory = ClassTransferFactory(session)

    def create_transfer(self, student_id: UUID, data: StudentClassTransferCreate) -> StudentClassTransferResponse:
        transfer = self.factory.create_transfer(student_id, data)
        return StudentClassTransferResponse.model_validate(transfer)

    def get_transfer(self, transfer_id: UUID) -> StudentClassTransferResponse:
        transfer = self.factory.get_transfer(transfer_id)
        return StudentClassTransferResponse.model_validate(transfer)

    def get_all_transfers(self, filters: ClassTransferFilterParams) -> List[StudentClassTransferResponse]:
        transfers = self.factory.get_all_transfers(filters)
        return [StudentClassTransferResponse.model_validate(t) for t in transfers]

    def update_transfer(self, transfer_id: UUID, data: StudentClassTransferUpdate) -> StudentClassTransferResponse:
        updated = self.factory.update_transfer(transfer_id, data.model_dump(exclude_unset=True))
        return StudentClassTransferResponse.model_validate(updated)

    def archive_transfer(self, transfer_id: UUID, reason: ArchiveReason) -> None:
        self.factory.archive_transfer(transfer_id, reason)

    def delete_transfer(self, transfer_id: UUID) -> None:
        self.factory.delete_transfer(transfer_id)

    def get_archived_transfer(self, transfer_id: UUID) -> StudentClassTransferResponse:
        archived = self.factory.get_archived_transfer(transfer_id)
        return StudentClassTransferResponse.model_validate(archived)

    def get_all_archived_transfers(self, filters: ClassTransferFilterParams) -> List[StudentClassTransferResponse]:
        transfers = self.factory.get_all_archived_transfers(filters)
        return [StudentClassTransferResponse.model_validate(t) for t in transfers]

    def restore_transfer(self, transfer_id: UUID) -> StudentClassTransferResponse:
        restored = self.factory.restore_transfer(transfer_id)
        return StudentClassTransferResponse.model_validate(restored)

    def delete_archived_transfer(self, transfer_id: UUID) -> None:
        self.factory.delete_archived_transfer(transfer_id)
