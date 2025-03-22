from .base_error import KademiaError
from datetime import date

class InputValidationError(KademiaError):
    """Base exception class for input-related errors."""

class EmptyFieldError(InputValidationError):
    """Raised when a required field is empty."""
    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = "Field cannot be empty"
        self.log_message = f"Domain: {domain}-- Input attempted with empty field: {entry}"

class BlankFieldError(InputValidationError):
    """Raised when a required field is blank (contains only whitespace)."""
    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = "Field cannot be blank"
        self.log_message = f"Domain: {domain}-- Input attempted with blank input: {entry}"

class TextTooShortError(InputValidationError):
    """Raised when text is too short, specifically when it has fewer than the minimum required characters."""
    def __init__(self, entry: str, min_length, domain=None):
        super().__init__()
        self.user_message = f"Text has to be {min_length} characters or more"
        self.log_message = f"Domain: {domain}-- Input attempted with short text: {entry}"

class DateError(InputValidationError):
    def __init__(self, date_input: date, domain=None):
        super().__init__()
        self.user_message = f"Date cannot be in the future"
        self.log_message = f"Domain: {domain}-- Input attempted with future date: {date_input}"

class InvalidCodeError(InputValidationError):
    """Raised when a code string has fewer than the minimum required characters."""
    def __init__(self, entry: str, length, domain=None):
        super().__init__()
        self.user_message = f"Code has to be exactly {length} alphabetical characters!"
        self.log_message = f"Domain: {domain}-- Input attempted with Invalid length: {entry}"

class InvalidCharacterError(InputValidationError):
    """Raised when an input contains a numeric value."""
    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = f"Field cannot contain a numeric character!"
        self.log_message = f"Domain: {domain}-- Input attempted with invalid character: {entry}"

class InvalidPhoneError(InputValidationError):
    """Raised when an input contains a numeric value."""
    def __init__(self, entry: str):
        super().__init__()
        self.user_message = f"Field cannot contain a numeric character!"
        self.log_message = f"Phone number entry attempted with invalid format: {entry}"


class InvalidSessionYearError(InputValidationError):
    """Raised when session year is in the past or too far into the future."""
    def __init__(self, entry: int, current_year):
        super().__init__()
        self.user_message = f"Session year has to be between {current_year} and {current_year+2}"
        self.log_message = f"Invalid session year entered: {entry}"
