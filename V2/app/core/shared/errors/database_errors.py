from .base_error import KademiaError
from uuid import UUID



class DBError(KademiaError):
    """Base exception class for all database related errors"""


class EntityNotFoundError(DBError):
    """Raised when an entity cannot be found in the database"""
    def __init__(self, entity_model, identifier: UUID, error: str, display_name: str ):

        self.user_message = f"{display_name} not found"
        self.log_message = f"{entity_model} not with id {identifier} not found. DETAIL: {error}"
        super().__init__()


class UniqueViolationError(DBError):
    """Raised when attempting to violate a unique constraint"""
    def __init__(self, error: str, constraint: str|None = None):
        self.error = error
        self.constraint = constraint or "unknown"
        self.user_message = "This record already exists"
        self.log_message = f"Unique constraint violation: {self.constraint} - {error}"
        super().__init__()


class DuplicateEntityError(UniqueViolationError):
    """Raised when creation of a duplicate entity is attempted."""
    def __init__(self, entity_model, entry: str, field: str, detail: str, display_name: str):
        super().__init__(error=detail)
        self.user_message = f"A {display_name} with {field} '{entry}' already exists"
        self.log_message = f"Duplicate {entity_model} creation: {detail}'"


class RelationshipError(DBError):
    """Raised when a foreign key constraint is violated during data operations"""

    def __init__(self, error: str, operation: str, constraint: str | None = None):
        self.error = error
        self.constraint = constraint or "unknown"
        self.user_message = f"Related record does not exist"
        self.log_message = f"ForeignKeyViolation: during {operation} - {error}"
        super().__init__()

    def __str__(self):
        return self.error


class RelatedEntityNotFoundError(RelationshipError):
    """Raised when an entity cannot be found during attempted fk insertion"""
    def __init__(
            self, entity_model, identifier: UUID, display_name: str, operation: str,
            detail: str):
        super().__init__(error=detail, operation=operation)

        self.user_message = f"Related {display_name} not found!"
        self.log_message = (f"Error during during fk insertion of {entity_model} with "
                            f"id:{identifier} during {operation}.")



class EntityInUseError(UniqueViolationError):
    """Raised when attempting to delete an entity that is referenced as a fk by another entity."""

    def __init__(self, entity_model, dependencies: str,  display_name: str, detail: str):
        super().__init__(error=detail)
        self.user_message = f"Cannot delete {display_name} while linked to {dependencies}"
        self.log_message = f"Deletion blocked: {entity_model} is still linked to {dependencies}. Detail: {detail}"


class NullFKConstraintMisconfiguredError (DBError):
    """Raised when a fk delete action is not set to NULL as expected"""

    def __init__(self, fk_name: str, entity_model, display_name: str):
        super().__init__()
        self.user_message = f"Error: Cannot delete {display_name}."
        self.log_message = (f"{entity_model} Deletion blocked: Foreign key constraint {fk_name} "
                            f"not set to NULL on delete")


class CascadeFKConstraintMisconfiguredError (DBError):
    """Raised when a fk delete action is not set as predicted"""

    def __init__(self, fk_name: str, entity_name: str):
        super().__init__()
        self.user_message = f"Error: Cannot delete {entity_name}."
        self.log_message = f"Deletion blocked: Foreign key constraint {fk_name} not set to CASCADE on delete"


class TransactionError(DBError):
    """Raised when a database transaction fails"""
    def __init__(self, operation: str = None):
        self.operation = operation
        self.user_message = "Operation could not be completed!"
        self.log_message = "Transaction failed"
        if self.operation:
            self.log_message += f" during {operation}"

        super().__init__()



class DBConnectionError(DBError):
    """Raised when database connection fails"""
    def __init__(self, error: str):
        self.error = error

        self.user_message = "Service temporarily unavailable"
        self.log_message = f"Database connection failed. Detail: {error}"
        super().__init__()



class DatabaseError(DBError):
    """For parent class database exceptions. """
    def __init__(self, error: str):
        self.user_message = "An unexpected error occurred"
        self.log_message = f"Database operation failed. Detail: {error}"

        super().__init__()

    def __str__(self):
        return self.log_message

