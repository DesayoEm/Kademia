from .base_error import KademiaError
from uuid import UUID

class ProgressionError(KademiaError):
    """Base exception class for all archive and deletion related exceptions"""


class InvalidPromotionLevelError(ProgressionError):
    """Raised when an invalid level is passed in during promotion"""

    def __init__(self, next_level_id: UUID, previous_level_id: UUID):
        super().__init__()
        self.user_message = f"Invalid promotion:Promotion must be to the next immediate level."
        self.log_message = f"Invalid promotion: id {next_level_id} is not the next level after {previous_level_id}"


class InvalidRepetitionLevelError(ProgressionError):
    """Raised when an invalid level is passed in during repetition"""

    def __init__(self, repeat_level_id: UUID, failed_level_id: UUID):
        super().__init__()
        self.user_message = f"Invalid repetition:Repetition must be to a lower level."
        self.log_message = f"Invalid repetition: id {repeat_level_id} is not less than {failed_level_id}"
