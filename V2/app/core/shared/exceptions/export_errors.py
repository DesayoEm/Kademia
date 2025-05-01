from .base_error import KademiaError

class ExportError(KademiaError):
    """Base exception for all export-related exceptions"""


class ExportFormatError(ExportError):
    """Raised when an unsupported export format is entered."""

    def __init__(self, format_entry):
        self.user_message = f"Unsupported export format!"
        self.log_message = f"Unsupported export format attempted: {format_entry}"

        super().__init__()

class UnimplementedGathererError(ExportError):
    """Raised when a data gatherer method is not called during exporting."""

    def __init__(self, entity):
        self.user_message = f"Failed to gather data!"
        self.log_message = f"No gatherer implemented for {entity}"

        super().__init__()


