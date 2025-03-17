from .base_error import KademiaError
from datetime import date

class InputError(KademiaError):
    """Base exception class for input-related errors."""

class EmptyFieldError(InputError):
    """Raised when a required field is empty."""
    def __init__(self, data: str, domain=None):
        super().__init__()
        domain_prefix = f"[{domain}] " if domain else ""
        self.user_message = "Field cannot be empty"
        self.log_message = f"{domain_prefix}Creation attempted with empty field: {data}"

class BlankFieldError(InputError):
    """Raised when a required field is blank (contains only whitespace)."""
    def __init__(self, data: str, domain=None):
        super().__init__()
        domain_prefix = f"[{domain}] " if domain else ""
        self.user_message = "Field cannot be blank"
        self.log_message = f"{domain_prefix}Creation attempted with blank input: {data}"

class TextTooShortError(InputError):
    """Raised when text is too short, specifically when it has fewer than the minimum required characters."""
    def __init__(self, data: str, min_length=3, domain=None):
        super().__init__()
        domain_prefix = f"[{domain}] " if domain else ""
        self.user_message = f"Text has to be {min_length} characters or more"
        self.log_message = f"{domain_prefix}Creation attempted with short text: {data}"

class DateError(InputError):
    def __init__(self, date_input: date, domain=None):
        super().__init__()
        domain_prefix = f"[{domain}] " if domain else ""
        self.user_message = f"Date cannot be in the future"
        self.log_message = f"{domain_prefix}Creation attempted with future date: {date_input}"


