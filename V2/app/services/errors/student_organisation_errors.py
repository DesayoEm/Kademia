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
    """Raised when user attempts a duplicate academic level field."""
    def __init__(self, input: str, original_error: Exception, field:str):
        UniqueViolationError.__init__(self, field_name=field, value=input)
        self.user_message = f"A level with {field} {input} already exists"
        if hasattr(original_error, 'log_message'):
            error_details = original_error.log_message
        else:
            error_details = str(original_error)
        self.log_message = f"Duplicate academic level creation attempted: {error_details}"

class LevelNotFoundError(StudentOrganizationError, EntityNotFoundError):
    """Raised when an academic level is not found."""
    def __init__(self, id: UUID):
        EntityNotFoundError.__init__(self, entity_type="Role", identifier=str(id))
        self.user_message = f"Academic level not found!"
        self.log_message = f"Academic level with id:{id} not found"

class DuplicateClassError(StudentOrganizationError, UniqueViolationError):
    """Raised when a duplicate class is created."""
    def __init__(self, input: str, original_error: Exception):
        UniqueViolationError.__init__(self, field_name="title", value=input)
        self.user_message = f"Class {input} already exists for this academic level"
        self.log_message = f"Duplicate class creation attempted: {original_error}"

class ClassNotFoundError(StudentOrganizationError, EntityNotFoundError):
    """Raised when a class is not found."""
    def __init__(self, id: UUID):
        EntityNotFoundError.__init__(self, entity_type="Role", identifier=str(id))
        self.user_message = f"Class not found!"
        self.log_message = f"Class with id:{id} not found"