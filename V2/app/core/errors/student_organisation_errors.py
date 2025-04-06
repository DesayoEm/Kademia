from .base_error import KademiaError
from .database_errors import EntityNotFoundError, UniqueViolationError, RelationshipError
from uuid import UUID


class StudentOrganizationError(KademiaError):
    """Base exception class for all exceptions related to student organization."""


class DuplicateStudentDepartmentError(StudentOrganizationError, UniqueViolationError):
    """Raised when a duplicate student department is created."""

    def __init__(self, entry: str, detail: str, field: str = "name"):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A student department with the {field} {entry} already exists"
        self.log_message = f"Duplicate student department creation attempted: {detail}"


class StudentDepartmentNotFoundError(StudentOrganizationError, EntityNotFoundError):
    """Raised when a department is not found."""

    def __init__(self, identifier: UUID, detail: str):
        EntityNotFoundError.__init__(self, entity_type="Department", identifier=str(identifier), error = detail)
        self.user_message = f"Department not found!"
        self.log_message = f"Department with id:{identifier} not found. DETAIL: {detail}"


class RelatedStudentDepartmentNotFoundError(StudentOrganizationError, RelationshipError):
    """Raised when a department is not found during fk insertion"""

    def __init__(self, identifier: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error = detail, operation=action, entity="Department")
        self.user_message = f"Related department not found!"
        self.log_message = f"Error during during fk insertion of department with id:{identifier} during {action} operation. Detail {detail}"


class StudentDepartmentInUseError(StudentOrganizationError, UniqueViolationError):
    """Raised when attempting to delete a department that still has related entities."""

    def __init__(self, entity_name: str, detail: str):
        super().__init__(error=detail)
        self.user_message = f"Cannot delete department while {entity_name} is still assigned."
        self.log_message = f"Deletion blocked: department is still linked to {entity_name}. Detail: {detail}"


class DuplicateLevelError(StudentOrganizationError, UniqueViolationError):
    """Raised when users attempts a duplicate academic level field."""

    def __init__(self, entry: str, detail: str, field: str ):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A level with {field} {entry} already exists"
        self.log_message = f"Duplicate level creation attempted: {detail}"


class LevelNotFoundError(StudentOrganizationError, EntityNotFoundError):
    """Raised when an academic level is not found."""

    def __init__(self, identifier: UUID, detail: str):
        EntityNotFoundError.__init__(self, entity_type="Department", identifier=str(identifier), error=detail)
        self.user_message = f"Academic level not found!"
        self.log_message = f"Academic level with id:{identifier} not found. DETAIL: {detail}"


class RelatedLevelNotFoundError(StudentOrganizationError, RelationshipError):
    """Raised when an academic level is not found during fk insertion"""

    def __init__(self, identifier: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error = detail, operation=action, entity="Academic Level")
        self.user_message = f"Related academic level not found!"
        self.log_message = f"Error during during fk insertion of Academic Level with id:{identifier} during {action} operation. Detail {detail}"


class LevelInUseError(StudentOrganizationError, UniqueViolationError):
    """Raised when attempting to delete an academic level that still has related entities."""

    def __init__(self, entity_name: str, detail: str):
        super().__init__(error=detail)
        self.user_message = f"Cannot delete academic level while {entity_name} is still assigned."
        self.log_message = f"Deletion blocked: academic level is still linked to {entity_name}. Detail: {detail}"


class DuplicateClassError(StudentOrganizationError, UniqueViolationError):
    """Raised when a duplicate class is created."""

    def __init__(self, entry: str, detail: str, field: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"{field} {entry} already exists for class"
        self.log_message = f"Duplicate class creation attempted: {detail}"


class ClassNotFoundError(StudentOrganizationError, EntityNotFoundError):
    """Raised when a class is not found."""

    def __init__(self, identifier: UUID, detail: str):
        EntityNotFoundError.__init__(self, entity_type="Department", identifier=str(identifier), error=detail)
        self.user_message = f"Class not found!"
        self.log_message = f"Class with id:{identifier} not found. DETAIL: {detail}"


class RelatedClassNotFoundError(StudentOrganizationError, RelationshipError):
    """Raised when a class is not found during fk insertion"""

    def __init__(self, identifier: UUID, detail: str, action: str):
        RelationshipError.__init__(self, error = detail, operation=action, entity="Class")
        self.user_message = f"Related class not found!"
        self.log_message = f"Error during during fk insertion of Academic Level with id:{identifier} during {action} operation. Detail {detail}"


class ClassInUseError(StudentOrganizationError, UniqueViolationError):
    """Raised when attempting to delete an academic level that still has related entities."""

    def __init__(self, entity_name: str, detail: str):
        super().__init__(error=detail)
        self.user_message = f"Cannot delete class while {entity_name} is still assigned."
        self.log_message = f"Deletion blocked: class is still linked to {entity_name}. Detail: {detail}"

