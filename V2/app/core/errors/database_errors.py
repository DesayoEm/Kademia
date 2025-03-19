from .base_error import KademiaError

class DBError(KademiaError):
    """Base exception class for all database related errors"""

class EntityNotFoundError(DBError):
    """Raised when an entity cannot be found in the database"""
    def __init__(self, entity_type: str, identifier: str, error: str ):
        self.entity_type = entity_type
        self.identifier = identifier
        self.error = error

        self.user_message = f"Record not found"
        self.log_message = f"{entity_type} not with id {identifier} not found. DETAIL: {error}"
        super().__init__()

    def __str__(self):
       return self.log_message


class UniqueViolationError(DBError):
    """Raised when attempting to violate a unique constraint"""
    def __init__(self, error: str):
        self.error = error
        self.user_message = "This record already exists"
        self.log_message = f"Unique constraint violation - Detail: {error}"

        super().__init__()

    def __str__(self):
        return self.log_message

class RelationshipError(DBError):
    """Raised when a foreign key constraint is violated during data operations"""
    def __init__(self, error: str, operation: str, entity: str):
        self.error = error
        self.user_message = f"Cannot {operation} record because related {entity} does not exist"
        self.log_message = f"Foreign key constraint violation during {operation} operation. Detail: {error}"

        super().__init__()

    def __str__(self):
        return self.log_message


class TransactionError(DBError):
    """Raised when a database transaction fails"""
    def __init__(self, operation: str = None):
        self.operation = operation
        self.user_message = "Operation could not be completed"
        self.log_message = "Transaction failed"
        if self.operation:
            self.log_message += f" during {operation}"

        super().__init__()

    def __str__(self):
       return self.log_message

class DBConnectionError(DBError):
    """Raised when database connection fails"""
    def __init__(self, error: str):
        self.error = error

        self.user_message = "Service temporarily unavailable"
        self.log_message = f"Database connection failed. Detail: {error}"
        super().__init__()

    def __str__(self):
       return self.log_message


class DatabaseError(DBError):
    """For parent class database exceptions. """
    def __init__(self, error: str):
        self.user_message = "An unexpected error occurred"
        self.log_message = f"Database operation failed. Detail: {error}"

        super().__init__(self.log_message)

    def __str__(self):
       return self.log_message