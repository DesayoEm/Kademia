from .base_error import KademiaError
from datetime import date


class EntryValidationError(KademiaError):
    """Base exception class for entry-related exceptions."""


class EmptyFieldError(EntryValidationError):
    """Raised when a required field is empty."""

    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = "Field cannot be empty"
        self.log_message = f"Domain: {domain}-- Entry attempted with empty field: {entry}"


class InvalidCharacterError(EntryValidationError):
    """Raised when a string entry contains a numeric value."""

    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = f"Field cannot contain a numeric character!"
        self.log_message = f"Domain: {domain}-- Entry attempted with invalid character: {entry}"


class TextTooShortError(EntryValidationError):
    """Raised when text is too short, specifically when it has fewer than the minimum required characters."""

    def __init__(self, entry: str, min_length, domain=None):
        super().__init__()
        self.user_message = f"Text has to be {min_length} characters or more"
        self.log_message = f"Domain: {domain}-- Entry attempted with short text: {entry}"


class TextTooLongError(EntryValidationError):
    """Raised when text is too long, specifically when it has more than the maximum required characters."""

    def __init__(self, entry: str, max_length: int, domain=None):
        super().__init__()
        self.user_message = f"Text has to be {max_length} characters or less"
        self.log_message = f"Domain: {domain}-- Entry attempted with LONG TEXT: {entry}."


class DBTextTooLongError(EntryValidationError):
    """Raised when long text validation is unhandled at the application layer and
    db(psycopg) raises a StringDataRightTruncation
    """

    def __init__(self, error: str):
        super().__init__()
        self.user_message = f"Text exceeds maximum allowed length for this field."
        self.log_message = f"Unhandled StringDataRightTruncation. Detail : {error}"

class PastYearError(EntryValidationError):
    """Raised when a year entry is in the past."""

    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = f"Year cannot be in the past!"
        self.log_message = f"Domain: {domain}-- Year Entry attempted with past year: {entry}"


class FutureYearError(EntryValidationError):
    """Raised when a year entry is in the future."""

    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = f"Year cannot be in the future!"
        self.log_message = f"Domain: {domain}-- Year Entry attempted with future year: {entry}"

class PastDateError(EntryValidationError):
    """Raised when a date entry is in the past."""

    def __init__(self, entry: date, domain = None):
        super().__init__()
        self.user_message = f"Date cannot be in the past"
        self.log_message = f"{domain}-Future date entered: {entry}"

class FutureDateError(EntryValidationError):
    """Raised when a date entry is in the future."""
    def __init__(self, entry: date, domain=None):
        super().__init__()
        self.user_message = f"Date cannot be in the future"
        self.log_message = f"Domain: {domain}-- Entry attempted with future date: {entry}"

class DateFormatError(EntryValidationError):
    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = f"Date input must be in the following format - YYYY-MM-DD"
        self.log_message = f"Domain: {domain}-- Entry attempted with invalid date: {entry}"

class SessionYearFormatError(EntryValidationError):
    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = f"Academic year must be in the format YYYY/YYYY"
        self.log_message = f"Domain: {domain}-- Session year attempted with invalid format: {entry}"

class InvalidSessionRangeError(EntryValidationError):
    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = f"Second year must be exactly one year after the first"
        self.log_message = f"Domain: {domain}-- Session year attempted with invalid format: {entry}"

class InvalidYearError(EntryValidationError):
    """Raised when a year input contains a non-numeric value."""

    def __init__(self, year: str, domain=None):
        super().__init__()
        self.user_message = f"Year cannot contain a non-numeric character!"
        self.log_message = f"Domain: {domain}-- Year Entry attempted with invalid character: {year}"

class InvalidYearLengthError(EntryValidationError):
    """Raised when a year entry contains more than 4 digits."""

    def __init__(self, year: str, domain=None):
        super().__init__()
        self.user_message = f"Year cannot contain a more than four digits!"
        self.log_message = f"Domain: {domain}-- Year Entry attempted with invalid length: {year}"


class InvalidOrderNumberError(EntryValidationError):
    """Raised when an order number fails validation."""

    def __init__(self, entry: int, domain=None):
        super().__init__()
        self.user_message = f"Order must be greater than 0!"
        self.log_message = f"Domain: {domain}-- Order entry attempted with Invalid integer: {entry}"


class InvalidPhoneError(EntryValidationError):
    """Raised when entered phone number is invalid."""

    def __init__(self, entry: str):
        super().__init__()
        self.user_message = f"Phone number must be in the following format: +[country code][number] (e.g., +2348056794506)"
        self.log_message = f"Phone number entry attempted with invalid format: {entry}"


class EmailFormatError(EntryValidationError):
    def __init__(self, entry: str):
        super().__init__()
        self.user_message = "Email must be in a valid format"
        self.log_message = f"Email setting attempted with invalid format: {entry}"

