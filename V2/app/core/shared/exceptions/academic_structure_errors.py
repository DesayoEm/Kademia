from .base_error import KademiaError


class StudentOrganizationError(KademiaError):
    """Base exception class for all exceptions related to student organization."""


class InvalidCodeError(StudentOrganizationError):
    """Raised when a department code string has fewer or more than the required characters."""

    def __init__(self, entry: str, length, domain=None):
        super().__init__()
        self.user_message = f"Code has to be exactly {length} alphabetical characters!"
        self.log_message = f"Domain: {domain}-- Input attempted with Invalid length: {entry}"


class InvalidOrderNumberError(StudentOrganizationError):
    """Raised when an order number fails validation."""

    def __init__(self, entry: int, domain=None):
        super().__init__()
        self.user_message = f"Order must be greater than 0!"
        self.log_message = f"Domain: {domain}-- Order entry attempted with Invalid integer: {entry}"


class InvalidRankNumberError(StudentOrganizationError):
    """Raised when a promotion rank number fails validation."""

    def __init__(self, entry: int, domain=None):
        super().__init__()
        self.user_message = f"Rank must be greater than 0!"
        self.log_message = f"Domain: {domain}-- Promotion rank entry attempted with Invalid integer: {entry}"
