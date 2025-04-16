from .base_error import KademiaError
from uuid import UUID

class ArchiveAndDeleteError(KademiaError):
    """Base exception class for all archive and deletion related errors"""


class CascadeDeletionError(ArchiveAndDeleteError):
    """Raised when an error occurs during a cascade deletion operation."""

    def __init__(self, error: str):
        self.user_message = f"Deletion failed!"
        self.log_message = f"Cascade deletion failed. DETAIL: {error} "

        super().__init__(f"")


class ArchiveDependencyError(ArchiveAndDeleteError):
    """Raised when attempting to archive an entity that is referenced by active records"""

    def __init__(self, entity_model, identifier: UUID, display_name: str,  related_entities: str):
        super().__init__()
        self.user_message = f"Cannot archive {display_name} while it is still linked to active {related_entities}."
        self.log_message = f"Deletion blocked: {entity_model}- id: {identifier} is still linked to {related_entities}"


class NullFKConstraintMisconfiguredError (ArchiveAndDeleteError):
    """Raised when a fk delete action is not set as predicted"""

    def __init__(self, fk_name: str, display_name: str):
        super().__init__()
        self.user_message = f"Error: Cannot delete {display_name}."
        self.log_message = f"Deletion blocked: Foreign key constraint {fk_name} not SET NULL"


class CascadeFKConstraintMisconfiguredError (ArchiveAndDeleteError):
    """Raised when a fk delete action is not set as predicted"""

    def __init__(self, fk_name: str, entity_name: str):
        super().__init__()
        self.user_message = f"Error: Cannot delete {entity_name}."
        self.log_message = f"Deletion blocked: Foreign key constraint {fk_name} not set to CASCADE"




