from .base_error import KademiaError

class AssessmentError(KademiaError):
    """Base exception class for assessment-related exceptions."""


class MaxScoreTooHighError(AssessmentError):
    def __init__(self, entry, domain):
        super().__init__()
        self.user_message = f"Max score '{entry}' exceeds maximum allowed score"
        self.log_message = f"Max score entry {entry} exceeds max. Domain: {domain}"


class ScoreExceedsMaxError(AssessmentError):
    def __init__(self, entry: int, max_score: int, domain):
        super().__init__()
        self.user_message = f"Score '{entry}' exceeds maximum allowed score"
        self.log_message = f"Score entry {entry} exceeds max ({max_score}). Domain: {domain}"


class InvalidWeightError(AssessmentError):
    def __init__(self, entry: int, cumulative_weight: int, domain):
        super().__init__()
        self.user_message = (f"Cumulative weight for the term can't exceed 100. "
                             f"Weight: {cumulative_weight}")
        self.log_message = (
            f"Weight entry {entry} caused cumulative weight {cumulative_weight} to exceed 100. "
            f"Domain: {domain}"
        )




