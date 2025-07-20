from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.core.transfer.factories.transfer import TransferFactory
from app.core.transfer.schemas.department_transfer import (
    StudentDepartmentTransferCreate,
    StudentDepartmentTransferResponse,
    DepartmentTransferFilterParams
)
from app.core.shared.schemas.enums import ArchiveReason


class StudentDepartmentTransferCrud:
    """CRUD operations for student department transfers."""

    def __init__(self, session: Session, current_user = None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.current_user = current_user
        self.factory = TransferFactory(session, current_user=current_user)


    def create_transfer(self, student_id: UUID, data: StudentDepartmentTransferCreate) -> StudentDepartmentTransferResponse:
        transfer = self.factory.create_transfer(student_id, data)
        return StudentDepartmentTransferResponse.model_validate(transfer)

    def get_transfer(self, transfer_id: UUID) -> StudentDepartmentTransferResponse:
        transfer = self.factory.get_transfer(transfer_id)
        return StudentDepartmentTransferResponse.model_validate(transfer)

    def get_all_transfers(self, filters: DepartmentTransferFilterParams) -> List[StudentDepartmentTransferResponse]:
        transfers = self.factory.get_all_transfers(filters)
        return [StudentDepartmentTransferResponse.model_validate(t) for t in transfers]


    def archive_transfer(self, transfer_id: UUID, reason: ArchiveReason) -> None:
        self.factory.archive_transfer(transfer_id, reason)

    def delete_transfer(self, transfer_id: UUID) -> None:
        self.factory.delete_transfer(transfer_id)

    def get_archived_transfer(self, archived_id: UUID) -> StudentDepartmentTransferResponse:
        archived = self.factory.get_archived_transfer(archived_id)
        return StudentDepartmentTransferResponse.model_validate(archived)

    def get_all_archived_transfers(self, filters: DepartmentTransferFilterParams) -> List[StudentDepartmentTransferResponse]:
        transfers = self.factory.get_all_archived_transfers(filters)
        return [StudentDepartmentTransferResponse.model_validate(t) for t in transfers]

    def restore_transfer(self, transfer_id: UUID) -> StudentDepartmentTransferResponse:
        restored = self.factory.restore_transfer(transfer_id)
        return StudentDepartmentTransferResponse.model_validate(restored)

    def delete_archived_transfer(self, transfer_id: UUID) -> None:
        self.factory.delete_archived_transfer(transfer_id)
