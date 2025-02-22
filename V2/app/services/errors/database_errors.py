from .base_error import TrakademikError

class DatabaseError(TrakademikError):
    """Base exception for all database operations"""
    def __init__(self, error: str = None):
        self.user_message = "An unexpected error occurred"
        self.log_message = f"Database operation failed on {error}"

        if error:
            self.log_message += f" on {error}"

        super().__init__(self.log_message)

    def __str__(self):
        return self.user_message


class EntityNotFoundError(DatabaseError):
    """Raised when an entity cannot be found in the database"""
    def __init__(self, entity_type: str, identifier: str = None):
        self.entity_type = entity_type
        self.identifier = identifier

        self.user_message = f"Requested {entity_type.lower()} not found"
        self.log_message = f"{entity_type} not found"
        if self.identifier:
            self.log_message += f" with identifier: {self.identifier}"
        super().__init__()

    def __str__(self):
        return self.user_message


class UniqueViolationError(DatabaseError):
    """Raised when attempting to violate a unique constraint"""
    def __init__(self, field_name: str, value: str = None):
        self.field_name = field_name
        self.value = value
        self.user_message = "This record already exists"
        self.log_message = f"Unique constraint violation for {field_name}"
        if self.value:
            self.log_message += f": {self.value}"

        super().__init__()

    def __str__(self):
        return self.user_message


class RelationshipError(DatabaseError):
    """Raised when a foreign key constraint is violated during data operations"""
    def __init__(self, relationship_name: str, operation: str = "update"):
        self.relationship_name = relationship_name
        self.user_message = f"Cannot {operation} record because related {relationship_name} does not exist"
        self.log_message =  f"Foreign key constraint violation on {relationship_name}"
        f"during {operation} operation"

        super().__init__()

    def __str__(self):
        return self.user_message



class TransactionError(DatabaseError):
    """Raised when a database transaction fails"""
    def __init__(self, operation: str = None):
        self.operation = operation
        self.user_message = "Operation could not be completed"
        self.log_message = "Transaction failed"
        if self.operation:
            self.log_message += f" during {operation}"

        super().__init__()

    def __str__(self):
        return self.user_message


class ConnectionError(DatabaseError):
    """Raised when database connection fails"""
    def __init__(self, details: str = None):
        self.details = details

        self.user_message = "Service temporarily unavailable"
        self.log_message = "Database connection failed"
        if self.details:
            self.log_message += f": {self.details}"

        super().__init__()

    def __str__(self):
        return self.user_message
