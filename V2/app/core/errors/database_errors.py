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


class RelatedEntityNotFoundError(DBError):
    """Raised when an entity cannot be found during attempted fk insertion"""
    def __init__(
            self, entity_model, identifier: UUID, display_name: str, operation: str):

        self.user_message = f"Related {display_name} not found!"
        self.log_message = (f"Error during during fk insertion of {entity_model} with "
                            f"id:{identifier} during {operation} operation.")
        super().__init__()


class UniqueViolationError(DBError):
    """Raised when attempting to violate a unique constraint"""
    def __init__(self, error: str):
        self.error = error
        self.user_message = "This record already exists"
        self.log_message = f"Unique constraint violation - Detail: {error}"

        super().__init__()


class DuplicateEntityError(UniqueViolationError):
    """Raised when creation of a duplicate entity is attempted."""

    def __init__(self, entity_model, entry: str, field: str, display_name: str, detail: str):
        UniqueViolationError.__init__(self, error=detail)
        self.user_message = f"A {display_name} with {field} {entry} already exists"
        self.log_message = f"Duplicate {entity_model} creation attempted: {detail}"


class EntityInUseError(UniqueViolationError):
    """Raised when attempting to delete an entity that is referenced as a fk by another entity."""

    def __init__(self, entity_model, dependencies: str, detail: str, display_name: str, ):
        super().__init__(error=detail)
        self.user_message = f"Cannot delete {display_name} while linked to {dependencies}"
        self.log_message = f"Deletion blocked: {entity_model} is still linked to {dependencies}. Detail: {detail}"


class RelationshipError(DBError):
    """Raised when a foreign key constraint is violated during data operations"""
    def __init__(self, error: str, operation: str, entity_model, domain: str):

        self.user_message = f"Cannot {operation} record because related {entity_model} does not exist"
        self.log_message = (f"Domain: {domain}Foreign key constraint violation during {operation} operation. "
                            f"Detail: {error}")

        super().__init__()


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

        super().__init__(self.log_message)

