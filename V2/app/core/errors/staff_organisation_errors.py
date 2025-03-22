from .base_error import KademiaError
from .input_validation_errors import TextTooShortError, EmptyFieldError, BlankFieldError, InvalidCharacterError
from .database_errors import EntityNotFoundError, UniqueViolationError, RelationshipError

from uuid import UUID

class StaffOrganizationError(KademiaError):
    """
    Base exception class for all exceptions related to staff organization.
    Inherits from KademiaError.
    """
    DOMAIN = "StaffOrganization"

# Domain-specific extensions of input validation errors
class StaffEmptyFieldError(EmptyFieldError):
    def __init__(self, input_value: str):
        super().__init__(data=input_value, domain=StaffOrganizationError.DOMAIN)

class StaffBlankFieldError(BlankFieldError):
    def __init__(self, input_value: str):
        super().__init__(data=input_value, domain=StaffOrganizationError.DOMAIN)

class StaffTextTooShortError(TextTooShortError):
    def __init__(self, input_value: str, min_length=3):
        super().__init__(data=input_value, min_length=min_length, domain=StaffOrganizationError.DOMAIN)

class StaffInvalidCharacterError(InvalidCharacterError):
    def __init__(self, input_value: str):
        super().__init__(data=input_value, domain=StaffOrganizationError.DOMAIN)



# Original domain-specific errors
class DuplicateDepartmentError(StaffOrganizationError, UniqueViolationError):
    """Raised when a duplicate department is created."""
    def __init__(self, input_value: str, detail: str, field: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A department with {field} {input_value} already exists"
        self.log_message = f"Duplicate department creation attempted: {detail}"

class DepartmentNotFoundError(StaffOrganizationError, EntityNotFoundError):
    """Raised when a department is not found."""
    def __init__(self, id: UUID, detail: str):
        EntityNotFoundError.__init__(self, entity_type="Department", identifier=str(id), error = detail)
        self.user_message = f"Department not found!"
        self.log_message = f"Department with id:{id} not found. Detail: {detail}"

class RelatedDepartmentNotFoundError(StaffOrganizationError, RelationshipError):
    """Raised when a department is not found during fk insertion"""
    def __init__(self, id: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error = detail, operation=action, entity="Academic Level")
        self.user_message = f"Related department not found!"
        self.log_message = f"Error during during fk insertion of staff department with id:{id} during {action} operation. Detail {detail}"


class DuplicateRoleError(StaffOrganizationError, UniqueViolationError):
    """Raised when a duplicate role is created."""
    def __init__(self, input_value: str, detail: str, field: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A role with {field} {input_value} already exists"
        self.log_message = f"Duplicate role creation attempted: {detail}"

class RoleNotFoundError(StaffOrganizationError, EntityNotFoundError):
    """Raised when a role is not found."""
    def __init__(self, id: UUID,  detail: str):
        EntityNotFoundError.__init__(self, entity_type="Role", identifier=str(id), error = detail)
        self.user_message = f"Role not found!"
        self.log_message = f"Role with id:{id} not found. Detail: {detail}"


class RelatedRoleNotFoundError(StaffOrganizationError, RelationshipError):
    """Raised when a role is not found during fk insertion"""

    def __init__(self, id: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error=detail, operation=action, entity="Academic Level")
        self.user_message = f"Related role not found!"
        self.log_message = f"Error during during fk insertion of role with id:{id} during {action} operation. Detail {detail}"


class DuplicateQualificationError(StaffOrganizationError, UniqueViolationError):
    """Raised when a duplicate qualification is created."""
    def __init__(self, input_value: str, detail: str, field: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A qualification with {field} {input_value} for this educator already exists"
        self.log_message = f"Duplicate qualification creation attempted. Detail {detail}"

class QualificationNotFoundError(StaffOrganizationError, EntityNotFoundError):
    """Raised when a qualification is not found."""
    def __init__(self, id: UUID, detail:str):
        EntityNotFoundError.__init__(self, entity_type="Qualification", identifier=str(id), error = detail)
        self.user_message = f"Qualification not found!"
        self.log_message = f"Qualification with id:{id} not found. Detail: {detail}"

