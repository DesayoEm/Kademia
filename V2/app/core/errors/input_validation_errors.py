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

class DBTextTooLongError(InputValidationError):
    """Raised when long text validation is unhandled at the application layer and
    db(psycopg) raises a StringDataRightTruncation
    """

    def __init__(self, error: str):
        super().__init__()
        self.user_message = f"Text exceeds maximum allowed length for this field."
        self.log_message = f"Unhandled StringDataRightTruncation. Detail : {error}"


class TextTooLongError(InputValidationError):
    """Raised when text is too long, specifically when it has more than the maximum required characters."""

    def __init__(self, entry: str, max_length: int, domain=None):
        super().__init__()
        self.user_message = f"Text has to be {max_length} characters or less"
        self.log_message = f"Domain: {domain}-- Input attempted with LONG TEXT: {entry}."


class DateError(InputValidationError):
    def __init__(self, date_input: date, domain=None):
        super().__init__()
        self.user_message = f"Date cannot be in the future"
        self.log_message = f"Domain: {domain}-- Input attempted with future date: {date_input}"


class DateFormatError(InputValidationError):
    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = f"Date input must be in the following format - YYYY-MM-DD"
        self.log_message = f"Domain: {domain}-- Entry attempted with invalid date: {entry}"


class PastDateError(InputValidationError):
    """Raised when a date input is in the past."""

    def __init__(self, entry: date, domain = None):
        super().__init__()
        self.user_message = f"Date cannot be in the past"
        self.log_message = f"{domain}-Future date entered: {entry}"


class InvalidValidityYearError(InputValidationError):
    """Raised when validity year is in the past."""

    def __init__(self, year: int):
        super().__init__()
        self.user_message = f"Validity year cannot be in the past"
        self.log_message = f"Invalid session year entered: {year}"


class InvalidYearError(InputValidationError):
    """Raised when a year input contains a non-numeric value."""

    def __init__(self, year: str, domain=None):
        super().__init__()
        self.user_message = f"Year cannot contain a non-numeric character!"
        self.log_message = f"Domain: {domain}-- Year input attempted with invalid character: {year}"


class InvalidYearLengthError(InputValidationError):
    """Raised when a year input contains more than 4 digits."""

    def __init__(self, year: str, domain=None):
        super().__init__()
        self.user_message = f"Year cannot contain a more than four digits!"
        self.log_message = f"Domain: {domain}-- Year input attempted with invalid length: {year}"


class InvalidSessionYearError(InputValidationError):
    """Raised when session year is in the past or too far into the future."""

    def __init__(self, entry: int, current_year):
        super().__init__()
        self.user_message = f"Session year has to be between {current_year} and {current_year+1}"
        self.log_message = f"Invalid session year entered: {entry}"



class InvalidCodeError(InputValidationError):
    """Raised when a code string has fewer than the minimum required characters."""

    def __init__(self, entry: str, length, domain=None):
        super().__init__()
        self.user_message = f"Code has to be exactly {length} alphabetical characters!"
        self.log_message = f"Domain: {domain}-- Input attempted with Invalid length: {entry}"

class InvalidOrderNumberError(InputValidationError):
    """Raised when an order number fails validation."""

    def __init__(self, entry: int, domain=None):
        super().__init__()
        self.user_message = f"Order must be greater than 0!"
        self.log_message = f"Domain: {domain}-- Order entry attempted with Invalid integer: {entry}"


class InvalidCharacterError(InputValidationError):
    """Raised when an input contains a numeric value."""

    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = f"Field cannot contain a numeric character!"
        self.log_message = f"Domain: {domain}-- Input attempted with invalid character: {entry}"

class InvalidPhoneError(InputValidationError):
    """Raised when entered phone number is invalid."""

    def __init__(self, entry: str):
        super().__init__()
        self.user_message = f"Phone number must be in the following format: +[country code][number] (e.g., +2348056794506)"
        self.log_message = f"Phone number entry attempted with invalid format: {entry}"


class EmailFormatError(InputValidationError):
    def __init__(self):
        self.user_message = "Email must be in a valid format"
        self.log_message = "Email setting attempted with invalid format"
        super().__init__()



