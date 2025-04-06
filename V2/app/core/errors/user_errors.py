from .base_error import KademiaError
from .database_errors import EntityNotFoundError, UniqueViolationError, RelationshipError
from uuid import UUID

class UserProfileError(KademiaError):
    """
    Base exception class for all exceptions related to profile data.
    """
    DOMAIN = "Profile"

#Staff-specific errors
class DuplicateStaffError(UserProfileError, UniqueViolationError):
    """Raised when duplicate data is entered for a unique constraint in the staff data."""

    def __init__(self, input_value: str, detail: str, field: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A Staff member with {field} {input_value} already exists"
        self.log_message = f"Duplicate staff creation attempted: {detail}"


class StaffNotFoundError(UserProfileError, EntityNotFoundError):
    """Raised when a staff account is not found."""

    def __init__(self, identifier: UUID, detail: str):
        EntityNotFoundError.__init__(self, entity_type="Staff", identifier=str(id), error = detail)
        self.user_message = f"Staff not found!"
        self.log_message = f"Staff with id:{identifier} not found. Detail {detail}"


class RelatedStaffNotFoundError(UserProfileError, RelationshipError):
    """Raised when a staff account is not found during fk insertion"""

    def __init__(self, identifier: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error = detail, operation=action, entity="Staff")
        self.user_message = f"Related staff not found!"
        self.log_message = f"Error during during fk insertion of Staff with id:{identifier} during {action} operation. Detail {detail}"


class RelatedEducatorNotFoundError(UserProfileError, RelationshipError):
    """Raised when an educator account is not found during fk insertion"""

    def __init__(self, identifier: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error = detail, operation=action, entity="Staff")
        self.user_message = f"Related educator not found!"
        self.log_message = f"Error during during fk insertion of Educator with id:{identifier} during {action} operation. Detail {detail}"


class StaffInUseError(UserProfileError, UniqueViolationError):
    """Raised when attempting to delete a staff member that still has related entities."""

    def __init__(self, entity_name: str, detail: str):
        super().__init__(error=detail)
        self.user_message = f"Cannot delete staff while {entity_name} is still assigned."
        self.log_message = f"Deletion blocked: staff is still linked to {entity_name}. Detail: {detail}"


class StaffTypeError(UserProfileError):
    """Raised when an invalid staff type is entered"""
    valid_types = ["Educator", "Admin", "Support"]
    def __init__(self, valid_types: list, input_value: str):
        self.user_message = f"Invalid staff_type: {input_value}. Valid types are: {valid_types}"
        self.log_message = f"Invalid staff type entered: {input_value}."




# Student-specific errors
class DuplicateStudentIDError(UserProfileError, UniqueViolationError):
    def __init__(self, stu_id: str, detail: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A student with id {stu_id} already exists!"
        self.log_message = f"Unique constraint violated during student creation with {stu_id}. Detail {detail}"


class DuplicateStudentError(UserProfileError, UniqueViolationError):
    def __init__(self, input_value: str, detail: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A student with {input_value} already exists!"
        self.log_message = f"Unique constraint violated during student creation with {input_value}. Detail {detail}"


class StudentNotFoundError(UserProfileError, EntityNotFoundError):
    """Raised when a staff account is not found."""
    def __init__(self, identifier: UUID, detail: str):
        EntityNotFoundError.__init__(self, entity_type="Student", identifier=str(identifier), error = detail)
        self.user_message = f"Student not found!"
        self.log_message = f"Student with id:{identifier} not found. Detail {detail}"


class RelatedStudentNotFoundError(UserProfileError, RelationshipError):
    """Raised when a student account is not found during fk insertion"""

    def __init__(self, identifier: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error = detail, operation=action, entity="Staff")
        self.user_message = f"Related student not found!"
        self.log_message = f"Error during during fk insertion of student with id:{identifier} during {action} operation. Detail {detail}"


class StudentInUseError(UserProfileError, UniqueViolationError):
    """Raised when attempting to delete a student that still has related entities."""

    def __init__(self, entity_name: str, detail: str):
        super().__init__(error=detail)
        self.user_message = f"Cannot delete student while {entity_name} is still assigned."
        self.log_message = f"Deletion blocked: student is still linked to {entity_name}. Detail: {detail}"


# Guardian-specific errors

class RelatedGuardianNotFoundError(UserProfileError, RelationshipError):
    """Raised when a guardian account is not found during fk insertion"""
    def __init__(self, identifier: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error = detail, operation=action, entity="Staff")
        self.user_message = f"Related guardian not found!"
        self.log_message = f"Error during during fk insertion of guardian with id:{identifier} during {action} operation. Detail {detail}"


class DuplicateGuardianError(UserProfileError, UniqueViolationError):
    def __init__(self, input_value: str, detail: str, field: str):
        UniqueViolationError.__init__(self,error=detail)
        self.user_message = f"A guardian with {field} {input_value} already exists!"
        self.log_message = f"Unique constraint violated for during guardian creation with {input_value}. Detail {detail}"


class GuardianNotFoundError(UserProfileError, EntityNotFoundError):
    """Raised when a staff account is not found."""
    def __init__(self, identifier: UUID, detail: str):
        EntityNotFoundError.__init__(self, entity_type="Guardian", identifier=str(identifier), error = detail)
        self.user_message = f"Guardian not found!"
        self.log_message = f"Guardian with id:{identifier} not found. Detail {detail}"
