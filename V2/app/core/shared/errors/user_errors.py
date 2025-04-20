from .base_error import KademiaError
from .database_errors import EntityNotFoundError, UniqueViolationError, RelationshipError


class IdentityError(KademiaError):
    """
    Base exception class for all exceptions related to profile data.
    """
    DOMAIN = "Profile"

#Staff-specific errors

class StaffTypeError(IdentityError):
    """Raised when an invalid staff type is entered"""
    valid_types = ["Educator", "Admin", "Support"]
    def __init__(self, valid_types: list, input_value: str):
        self.user_message = f"Invalid staff_type: {input_value}. Valid types are: {valid_types}"
        self.log_message = f"Invalid staff type entered: {input_value}."


# Student-specific errors
class DuplicateStudentIDError(IdentityError, UniqueViolationError):
    def __init__(self, stu_id: str, detail: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A student with id {stu_id} already exists!"
        self.log_message = f"Unique constraint violated during student creation with {stu_id}. Detail {detail}"


class InvalidSessionYearError(IdentityError):
    """Raised when session year is in the past or too far into the future."""

    def __init__(self, entry: int, current_year):
        super().__init__()
        self.user_message = f"Session year has to be between {current_year} and {current_year+1}"
        self.log_message = f"Invalid session year entered: {entry}"

