from .base_error import KademiaError
from uuid import UUID

class TransferError(KademiaError):
    """Base exception class for all transfer exceptions"""

class TransferStatusAlreadySetError(TransferError):
    """Raised when attempting to set a transfer status that's already been set."""

    def __init__(self, current_status: str, attempted_status: str, transfer_id: UUID):
        super().__init__()
        self.user_message = f"Transfer has already been {current_status.lower()}"
        self.log_message = f"Attempted to set status to {attempted_status} for transfer \
                        {transfer_id} that is already {current_status}"



class DepartmentNotSetError(TransferError):
    """Raised when attempting to transfer a student that has no department."""

    def __init__(self, student_id: UUID):
        super().__init__()
        self.user_message = f"Transfer error: Student does not belong to a department"
        self.log_message = f"Attempted to transfer student {student_id} who does not \
                        belong to a department"