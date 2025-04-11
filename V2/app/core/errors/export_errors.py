from .base_error import KademiaError

class ExportError(KademiaError):
    """Base exception for all export-related errors"""


class UnimplementedGathererError(ExportError):
    """Raised when a gather method is not called."""

    def __init__(self, entity):
        self.user_message = f"Failed to gather data!"
        self.log_message = f"No gatherer implemented for {entity}"

        super().__init__()


