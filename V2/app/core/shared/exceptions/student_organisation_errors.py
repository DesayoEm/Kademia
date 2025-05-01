from .base_error import KademiaError


class StudentOrganizationError(KademiaError):
    """Base exception class for all exceptions related to student organization."""


class InvalidCodeError(StudentOrganizationError):
    """Raised when a department code string has fewer or more than the required characters."""

    def __init__(self, entry: str, length, domain=None):
        super().__init__()
        self.user_message = f"Code has to be exactly {length} alphabetical characters!"
        self.log_message = f"Domain: {domain}-- Input attempted with Invalid length: {entry}"

