from .base_error import KademiaError
from .database_errors import EntityNotFoundError, UniqueViolationError, RelationshipError
from .archive_delete_errors import DeletionDependencyError, ForeignKeyConstraintMisconfiguredError

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

    def __init__(self, entry: str, detail: str, field: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A department with {field} {entry} already exists"
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

# Staff Roles

class DuplicateRoleError(StaffOrganizationError, UniqueViolationError):
    """Raised when a duplicate role is created."""

    def __init__(self, entry: str, detail: str, field: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A role with {field} {entry} already exists"
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


class RoleArchivalDependencyError(StaffOrganizationError):
    """Raised when attempting to archive a role that still has related active staff."""

    def __init__(self, entity_name: str, identifier: str):
        super().__init__()
        self.user_message = f"Cannot archive role while it is still assigned to active {entity_name}."
        self.log_message = f"Archival blocked: role {identifier} is still linked to {entity_name}"


class RoleDeletionDependencyError(StaffOrganizationError, DeletionDependencyError):
    """Raised when attempting to delete a role that still has related active entities."""

    def __init__(self, entity_name: str, identifier: UUID, related_entities: str):
        super().__init__(
            entity_name="role", identifier=identifier, related_entities=related_entities
        )
        self.user_message = f"Cannot delete {entity_name} while it is still assigned to {related_entities}."
        self.log_message = f"Deletion blocked: role {identifier} is still linked to {entity_name}"


class RoleDeletionConstraintError(StaffOrganizationError, ForeignKeyConstraintMisconfiguredError):
    """Raised when attempting to delete an entity that's not srt to null on delete"""

    def __init__(self, fk_name: str, display_name: str = 'role'):
        super().__init__(
            fk_name = fk_name, entity_name = display_name
        )
        self.user_message = f"Error: Cannot delete {display_name}."
        self.log_message = f"Deletion blocked: Foreign key constraint {fk_name} not SET NULL for safe deletion"



# Qualifications
class DuplicateQualificationError(StaffOrganizationError, UniqueViolationError):
    """Raised when a duplicate qualification is created."""

    def __init__(self, entry: str, detail: str, field: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A qualification with {field} {entry} for this educator already exists"
        self.log_message = f"Duplicate qualification creation attempted. Detail {detail}"


class QualificationNotFoundError(StaffOrganizationError, EntityNotFoundError):
    """Raised when a qualification is not found."""

    def __init__(self, identifier: UUID, detail:str):
        EntityNotFoundError.__init__(self, entity_type="Qualification", identifier=str(identifier), error = detail)
        self.user_message = f"Qualification not found!"
        self.log_message = f"Qualification with id:{identifier} not found. Detail: {detail}"


class QualificationInUseError(StaffOrganizationError, UniqueViolationError):
    """Raised when attempting to delete a qualification that still has related entities."""

    def __init__(self, entity_name: str, detail: str):
        super().__init__(error=detail)
        self.user_message = f"Cannot delete qualification while {entity_name} is still assigned."
        self.log_message = f"Deletion blocked: qualification is still linked to {entity_name}. Detail: {detail}"


class LifetimeValidityConflictError(StaffOrganizationError):
    """
    Raised when a 'Lifetime' validity type is selected
       but an invalid date or non-'Lifetime' value is provided for the valid_until field.
    """

    def __init__(self, entry):
        super().__init__()
        self.user_message = f"Valid until field must 'lifetime' if validity type is lifetime"
        self.log_message = f" Lifetime validity Entry attempted with invalid str: {entry}"


class TemporaryValidityConflictError(StaffOrganizationError):
    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = (
            "If validity type is temporary, "
            "Valid until field must be in the following date format - YYYY-MM-DD"
        )
        self.log_message = f"Domain: {domain}-- Entry attempted with invalid date: {entry}"
