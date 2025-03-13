from .base_error import TrakademikError
from .input_errors import TextTooShortError, EmptyFieldError, BlankFieldError
from .database_errors import EntityNotFoundError, UniqueViolationError
from uuid import UUID

class StaffOrganizationError(TrakademikError):
    """
    Base exception class for all exceptions related to staff organization.
    Inherits from TrakademikError.
    """
    DOMAIN = "StaffOrganization"

# Domain-specific extensions of input errors
class StaffEmptyFieldError(EmptyFieldError):
    def __init__(self, input: str):
        super().__init__(input=input, domain=StaffOrganizationError.DOMAIN)

class StaffBlankFieldError(BlankFieldError):
    def __init__(self, input: str):
        super().__init__(input=input, domain=StaffOrganizationError.DOMAIN)

class StaffTextTooShortError(TextTooShortError):
    def __init__(self, input: str, min_length=3):
        super().__init__(input=input, min_length=min_length, domain=StaffOrganizationError.DOMAIN)

# Original domain-specific errors
class DuplicateDepartmentError(StaffOrganizationError, UniqueViolationError):
    """Raised when a duplicate department is created."""
    def __init__(self, input: str, original_error: Exception):
        UniqueViolationError.__init__(self, field_name="name", value=input)
        self.user_message = f"A department with name {input} already exists"
        self.log_message = f"Duplicate department creation attempted: {original_error}"

class DepartmentNotFoundError(StaffOrganizationError, EntityNotFoundError):
    """Raised when a department is not found."""
    def __init__(self, id: UUID):
        EntityNotFoundError.__init__(self, entity_type="Department", identifier=str(id))
        self.user_message = f"Department not found!"
        self.log_message = f"Department with id:{id} not found"

class DuplicateRoleError(StaffOrganizationError, UniqueViolationError):
    """Raised when a duplicate role is created."""
    def __init__(self, name: str, original_error: Exception):
        UniqueViolationError.__init__(self, field_name="title", value=name)
        self.user_message = f"A role with name {name} already exists"
        self.log_message = f"Duplicate role creation attempted: {original_error}"

class RoleNotFoundError(StaffOrganizationError, EntityNotFoundError):
    """Raised when a role is not found."""
    def __init__(self, id: UUID):
        EntityNotFoundError.__init__(self, entity_type="Role", identifier=str(id))
        self.user_message = f"Role not found!"
        self.log_message = f"Role with id:{id} not found"

class DuplicateQualificationError(StaffOrganizationError, UniqueViolationError):
    """Raised when a duplicate qualification is created."""
    def __init__(self, name: str, original_error: Exception):
        UniqueViolationError.__init__(self, field_name="title", value=name)
        self.user_message = f"A qualification with name {name} for this educator already exists"
        self.log_message = f"Duplicate qualification creation attempted: {original_error}"

class QualificationNotFoundError(StaffOrganizationError, EntityNotFoundError):
    """Raised when a qualification is not found."""
    def __init__(self, id: UUID):
        EntityNotFoundError.__init__(self, entity_type="Qualification", identifier=str(id))
        self.user_message = f"Qualification not found!"
        self.log_message = f"Qualification with id:{id} not found"

