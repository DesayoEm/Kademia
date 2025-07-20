from .base_error import KademiaError
from uuid import UUID

class ProgressionError(KademiaError):
    """Base exception class for all progression related exceptions"""


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


class ProgressionStatusAlreadySetError(ProgressionError):
    """Raised when attempting to set a progression status that's already been set."""

    def __init__(
            self, progression_type: str, current_status: str,
            attempted_status: str, progression_id: UUID):
        super().__init__()
        self.user_message = f"{progression_type} has already been {current_status.lower()}"
        self.log_message = f"Attempted to set status to {attempted_status} for {progression_type} \
                        {progression_id} that is already {current_status}"


class LevelNotFinalError(ProgressionError):
    def __init__(self, level_id: UUID):
        super().__init__()
        self.user_message = f"Invalid graduation:Student must be in final level to graduate."
        self.log_message = f"Invalid graduation: id {level_id} is not a final level"
