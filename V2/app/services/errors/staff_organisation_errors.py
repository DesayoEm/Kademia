from .base_error import TrakademikError
from .database_errors import EntityNotFoundError, UniqueViolationError
from uuid import UUID

class StaffOrganizationError(TrakademikError):
    """
    Base exception class for all exceptions related to staff organization.
    Inherits from TrakademikError.
    """
    pass

class DuplicateDepartmentError(StaffOrganizationError, UniqueViolationError):
    """Raised when a duplicate department is created."""
    def __init__(self, name: str, original_error: Exception):
        UniqueViolationError.__init__(self, field_name="name", value=name)
        self.user_message = f"A department with name {name} already exists"
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

class EmptyFieldError(StaffOrganizationError):
    """Raised when a name field is empty."""
    def __init__(self, input):
        super().__init__()
        self.user_message = "Field cannot be empty"
        self.log_message = f"Entity creation attempted without name : {input}"

class BlankFieldError(StaffOrganizationError):
    """Raised when a name field is blank (contains only whitespace)."""
    def __init__(self, input: str):
        super().__init__()
        self.user_message = "Field cannot be blank"
        self.log_message = f"Entity creation attempted with blank name : {input}"

class TextTooShortError(StaffOrganizationError):
    """Raised when a name is too short, specifically when it has two or fewer characters."""
    def __init__(self, input: str):
        super().__init__()
        self.user_message = "Text has to be three characters or more"
        self.log_message = f"Entity creation attempted with short name : {input}"