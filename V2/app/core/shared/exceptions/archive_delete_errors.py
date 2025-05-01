from .base_error import KademiaError
from uuid import UUID

class ArchiveAndDeleteError(KademiaError):
    """Base exception class for all archive and deletion related exceptions"""


class CascadeDeletionError(ArchiveAndDeleteError):
    """Raised when an error occurs during a cascade deletion operation."""

    def __init__(self, error: str):
        super().__init__(f"")

        self.user_message = f"Deletion failed!"
        self.log_message = f"Cascade deletion failed. DETAIL: {error} "




class ArchiveDependencyError(ArchiveAndDeleteError):
    """Raised when attempting to archive an entity that is referenced by active records"""

    def __init__(self, entity_model, identifier: UUID, display_name: str,  related_entities: str):
        super().__init__()
        self.user_message = f"Cannot archive {display_name} while it is still linked to active {related_entities}."
        self.log_message = f"Deletion blocked: {entity_model}- id: {identifier} is still linked to {related_entities}"




