from .base_error import KademiaError
from .database_errors import EntityNotFoundError, UniqueViolationError, RelationshipError

from uuid import UUID

class StaffOrganizationError(KademiaError):
    """
    Base exception class for all exceptions related to staff organization.
    Inherits from KademiaError.
    """
    DOMAIN = "StaffOrganization"


# Original domain-specific errors
class DuplicateDepartmentError(StaffOrganizationError, UniqueViolationError):
    """Raised when a duplicate department is created."""

    def __init__(self, input_value: str, detail: str, field: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A department with {field} {input_value} already exists"
        self.log_message = f"Duplicate department creation attempted: {detail}"


class DepartmentInUseError(StaffOrganizationError, UniqueViolationError):
    """Raised when attempting to delete a department that still has related entities."""

    def __init__(self, entity_name: str, detail: str):
        super().__init__(error=detail)
        self.user_message = f"Cannot delete department while {entity_name} are still assigned."
        self.log_message = f"Deletion blocked: department is still linked to {entity_name}. Detail: {detail}"

class DepartmentNotFoundError(StaffOrganizationError, EntityNotFoundError):

    """Raised when a department is not found."""
    def __init__(self, identifier: UUID, detail: str):
        EntityNotFoundError.__init__(self, entity_type="Department", identifier=str(identifier), error = detail)
        self.user_message = f"Department not found!"
        self.log_message = f"Department with id:{identifier} not found. Detail: {detail}"


class RelatedDepartmentNotFoundError(StaffOrganizationError, RelationshipError):
    """Raised when a department is not found during fk insertion"""

    def __init__(self, identifier: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error = detail, operation=action, entity="Academic Level")
        self.user_message = f"Related department not found!"
        self.log_message = f"Error during during fk insertion of staff department with id:{identifier} during {action} operation. Detail {detail}"


class DuplicateRoleError(StaffOrganizationError, UniqueViolationError):
    """Raised when a duplicate role is created."""

    def __init__(self, input_value: str, detail: str, field: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A role with {field} {input_value} already exists"
        self.log_message = f"Duplicate role creation attempted: {detail}"


class RoleNotFoundError(StaffOrganizationError, EntityNotFoundError):
    """Raised when a role is not found."""

    def __init__(self, identifier: UUID,  detail: str):
        EntityNotFoundError.__init__(self, entity_type="Role", identifier=str(identifier), error = detail)
        self.user_message = f"Role not found!"
        self.log_message = f"Role with id:{identifier} not found. Detail: {detail}"


class RelatedRoleNotFoundError(StaffOrganizationError, RelationshipError):
    """Raised when a role is not found during fk insertion"""
    def __init__(self, identifier: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error=detail, operation=action, entity="Academic Level")
        self.user_message = f"Related role not found!"
        self.log_message = f"Error during during fk insertion of role with id:{identifier} during {action} operation. Detail {detail}"


class DuplicateQualificationError(StaffOrganizationError, UniqueViolationError):
    """Raised when a duplicate qualification is created."""
    def __init__(self, input_value: str, detail: str, field: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A qualification with {field} {input_value} for this educator already exists"
        self.log_message = f"Duplicate qualification creation attempted. Detail {detail}"


class QualificationNotFoundError(StaffOrganizationError, EntityNotFoundError):
    """Raised when a qualification is not found."""
    def __init__(self, identifier: UUID, detail:str):
        EntityNotFoundError.__init__(self, entity_type="Qualification", identifier=str(identifier), error = detail)
        self.user_message = f"Qualification not found!"
        self.log_message = f"Qualification with id:{id} not found. Detail: {detail}"


class QualificationInUseError(StaffOrganizationError, UniqueViolationError):
    """Raised when attempting to delete a qualification that still has related entities."""

    def __init__(self, entity_name: str, detail: str):
        super().__init__(error=detail)
        self.user_message = f"Cannot delete qualification while {entity_name} is still assigned."
        self.log_message = f"Deletion blocked: qualification is still linked to {entity_name}. Detail: {detail}"
