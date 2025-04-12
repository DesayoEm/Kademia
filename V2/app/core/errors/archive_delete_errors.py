from .base_error import KademiaError


class ArchiveAndDeleteError(KademiaError):
    """Base exception class for all archive and deletion related errors"""


class CascadeDeletionError(ArchiveAndDeleteError):
    """Raised when an error occurs during a cascade deletion operation."""

    def __init__(self, error: str):
        self.user_message = f"Deletion failed!"
        self.log_message = f"Cascade deletion failed. DETAIL: {error} "

        super().__init__(f"")


class DeletionDependencyError(ArchiveAndDeleteError):
    """Raised when attempting to delete an entity that has related records"""

    def __init__(self, entity_name: str, identifier: str):
        super().__init__()
        self.user_message = f"Cannot delete role while it is still assigned to {entity_name}."
        self.log_message = f"Deletion blocked: entity {identifier} is still linked to {entity_name}"

