from .base_error import KademiaError
from .database_errors import EntityNotFoundError, UniqueViolationError, RelationshipError
from .input_errors import TextTooShortError, EmptyFieldError, BlankFieldError, DateError
from uuid import UUID
from datetime import date


class ProfileError(KademiaError):
    """
    Base exception class for all exceptions related to profile data.
    """
    DOMAIN = "Profile"

# Domain-specific extensions of input errors
class ProfileEmptyFieldError(EmptyFieldError):
    def __init__(self, input_value: str):
        super().__init__(data=input_value, domain=ProfileError.DOMAIN)


class ProfileBlankFieldError(BlankFieldError):
    def __init__(self, input_value: str):
        super().__init__(data=input_value, domain=ProfileError.DOMAIN)


class ProfileTextTooShortError(TextTooShortError):
    def __init__(self, input_value: str, min_length=None):
        super().__init__(data=input_value, min_length=min_length, domain=ProfileError.DOMAIN)

class ProfileDateError(DateError):
    def __init__(self, data: date):
        super().__init__(date_input=data, domain=ProfileError.DOMAIN)


#Staff-specific errors
class DuplicateStaffError(ProfileError, UniqueViolationError):
    """Raised when duplicate data is entered for a unique constraint in the staff data."""
    def __init__(self, input_value: str, detail: str, field: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A Staff member with {field} {input_value} already exists"
        self.log_message = f"Duplicate staff creation attempted: {detail}"

class StaffNotFoundError(ProfileError, EntityNotFoundError):
    """Raised when a staff account is not found."""
    def __init__(self, id: UUID, detail: str):
        EntityNotFoundError.__init__(self, entity_type="Staff", identifier=str(id), error = detail)
        self.user_message = f"Staff not found!"
        self.log_message = f"Staff with id:{id} not found. Detail {detail}"

class RelatedStaffNotFoundError(ProfileError, RelationshipError):
    """Raised when a staff account is not found during fk insertion"""
    def __init__(self, id: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error = detail, operation=action, entity="Staff")
        self.user_message = f"Related staff not found!"
        self.log_message = f"Error during during fk insertion of Staff with id:{id} during {action} operation. Detail {detail}"

class RelatedEducatorNotFoundError(ProfileError, RelationshipError):
    """Raised when an educator account is not found during fk insertion"""
    def __init__(self, id: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error = detail, operation=action, entity="Staff")
        self.user_message = f"Related educator not found!"
        self.log_message = f"Error during during fk insertion of Educator with id:{id} during {action} operation. Detail {detail}"

# Student-specific errors
class DuplicateStudentIDError(ProfileError):
    def __init__(self, stu_id):
        self.stu_id = stu_id
        super().__init__(f'A student with id {stu_id} already exists')

class StudentNotFoundError(ProfileError):
    def __init__(self):
        super().__init__(f'Student not found!')

class StudentIdFormatError(ProfileError):
    def __init__(self):
        super().__init__("Please use correct id format (STU/00/00/0000)")


class RelatedStudentNotFoundError(ProfileError, RelationshipError):
    """Raised when a staff account is not found during fk insertion"""
    def __init__(self, id: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error = detail, operation=action, entity="Staff")
        self.user_message = f"Related staff not found!"
        self.log_message = f"Error during during fk insertion of Staff with id:{id} during {action} operation. Detail {detail}"

