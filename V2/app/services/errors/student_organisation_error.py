from .base_error import TrakademikError
from .database_errors import EntityNotFoundError, UniqueViolationError
from uuid import UUID
from .input_errors import EmptyFieldError, BlankFieldError, TextTooShortError

class StudentOrganizationError(TrakademikError):
    """
    Base exception class for all exceptions related to student organization.
    Inherits from TrakademikError.
    """
    DOMAIN = "StudentOrganization"

# Domain-specific extensions of validation errors
class StudentEmptyFieldError(EmptyFieldError):
    def __init__(self, input: str):
        super().__init__(input=input, domain=StudentOrganizationError.DOMAIN)

class StudentBlankFieldError(BlankFieldError):
    def __init__(self, input: str):
        super().__init__(input=input, domain=StudentOrganizationError.DOMAIN)

class StudentTextTooShortError(TextTooShortError):
    def __init__(self, input: str, min_length=3):
        super().__init__(input=input, min_length=min_length, domain=StudentOrganizationError.DOMAIN)


# Original domain-specific errors

class DuplicateStudentDepartmentError(StudentOrganizationError, UniqueViolationError):
    """Raised when a duplicate student department is created."""
    def __init__(self, input: str, original_error: Exception):
        UniqueViolationError.__init__(self, field_name="name", value=input)
        self.user_message = f"A student department with the name {input} already exists"
        self.log_message = f"Duplicate student department creation attempted: {original_error}"

class StudentDepartmentNotFoundError(StudentOrganizationError, EntityNotFoundError):
    """Raised when a department is not found."""
    def __init__(self, id: UUID):
        EntityNotFoundError.__init__(self, entity_type="Department", identifier=str(id))
        self.user_message = f"Department not found!"
        self.log_message = f"Department with id:{id} not found"

class DuplicateLevelError(StudentOrganizationError, UniqueViolationError):
    """Raised when a duplicate academic level is created."""
    def __init__(self, name: str, original_error: Exception):
        UniqueViolationError.__init__(self, field_name="title", value=name)
        self.user_message = f"A level with name {name} already exists"
        self.log_message = f"Duplicate academic level creation attempted: {original_error}"

class LevelNotFoundError(StudentOrganizationError, EntityNotFoundError):
    """Raised when an academic level is not found."""
    def __init__(self, id: UUID):
        EntityNotFoundError.__init__(self, entity_type="Role", identifier=str(id))
        self.user_message = f"Academic level not found!"
        self.log_message = f"Academic level with id:{id} not found"

