from .base_error import KademiaError
from uuid import UUID


class AssessmentError(KademiaError):
    """Base exception class for assessment-related exceptions."""


class MaxScoreTooHighError(AssessmentError):
    def __init__(self, entry):
        super().__init__()
        self.user_message = f"Max score '{entry}' exceeds maximum allowed score"
        self.log_message = f"Max score entry {entry} exceeds max."


class WeightTooHighError(AssessmentError):
    def __init__(self, entry):
        super().__init__()
        self.user_message = f"Weight '{entry}' exceeds maximum allowed score"
        self.log_message = f"Weight entry {entry} exceeds max."


class ScoreExceedsMaxError(AssessmentError):
    def __init__(self, entry: int, max_score: int):
        super().__init__()
        self.user_message = f"Score '{entry}' exceeds maximum allowed score"
        self.log_message = f"Score entry {entry} exceeds max ({max_score})."


class UnableToRecalculateError(AssessmentError):
    def __init__(self, total_grade_id: UUID, error: str):
        super().__init__()
        self.user_message = f"Update successful but unable to recalculate total grades"
        self.log_message = f"Update successful but unable to recalculate total grades for \
            {str(total_grade_id)}: {error})."


class InvalidWeightError(AssessmentError):
    def __init__(self, entry: int, cumulative_weight: int):
        super().__init__()
        self.user_message = (
            f"Cumulative weight for the semester can't exceed 10. "
            f"Total weight left: {10- cumulative_weight}"
        )
        self.log_message = f"Weight entry {entry} caused cumulative weight {cumulative_weight} to exceed 10"


class FileAlreadyExistsError(AssessmentError):
    def __init__(self, obj_id: UUID):
        super().__init__()
        self.user_message = (
            f"There's a file associated with this grade object. \""
            f"Please remove it to upload a new one"
        )
        self.log_message = f"File already exists for object ({obj_id})."
