from .base_error import KademiaError
from .database_errors import EntityNotFoundError, UniqueViolationError
from .input_errors import TextTooShortError, EmptyFieldError, BlankFieldError
from uuid import UUID
from datetime import date


class ProfileError(KademiaError):
    """
    Base exception class for all exceptions related to profile data..
    """
    DOMAIN = "Staff Profile"

# Domain-specific extensions of input errors
class StaffEmptyFieldError(EmptyFieldError):
    def __init__(self, input_value: str):
        super().__init__(data=input_value, domain=ProfileError.DOMAIN)


class StaffBlankFieldError(BlankFieldError):
    def __init__(self, input_value: str):
        super().__init__(data=input_value, domain=ProfileError.DOMAIN)


class StaffTextTooShortError(TextTooShortError):
    def __init__(self, input_value: str, min_length=None):
        super().__init__(data=input_value, min_length=min_length, domain=ProfileError.DOMAIN)

#Domain-specific errors
class DuplicateStaffError(ProfileError, UniqueViolationError):
    """Raised when duplicate data is entered for a unique constraint in the staff data."""
    def __init__(self, input_value: str, detail: str, field: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A Staff member with {field} {input_value} already exists"
        self.log_message = f"Duplicate staff creation attempted: {detail}"

class StaffNotFoundError(ProfileError, EntityNotFoundError):
    """Raised when a staff account is not found."""
    def __init__(self, id: UUID):
        EntityNotFoundError.__init__(self, entity_type="Staff", identifier=str(id))
        self.user_message = f"Staff not found!"
        self.log_message = f"Staff with id:{id} not found"


class DateError(ProfileError):
    def __init__(self, input_date: date):
        self.user_message = f"Date cannot be in the future!"
        self.log_message = f"future date entry attempted. Entry: {input_date}"
       


