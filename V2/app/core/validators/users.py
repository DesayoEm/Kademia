from datetime import date, datetime
import re

from ..errors.user_errors import InvalidSessionYearError
from ...core.errors.entry_validation_errors import(
 TextTooShortError,EmptyFieldError, InvalidCharacterError, InvalidPhoneError, FutureDateError
    )
class UserValidator:
    def __init__(self):
        self.domain = "USER PROFILE"

    def validate_name(self, value:str):
        value = (value or "").strip()
        if not value:
            raise EmptyFieldError(entry=value, domain=self.domain)

        if len(value.strip()) < 2:
            raise TextTooShortError(entry = value, domain = self.domain, min_length = 2)
        if any(val.isnumeric() for val in value):
            raise InvalidCharacterError(entry=value, domain=self.domain)

        return value.title()


    def validate_address(self, value:str):
        value = (value or "").strip()
        if not value:
            raise EmptyFieldError(entry=value, domain=self.domain)
        if len(value.strip()) < 12:
            raise TextTooShortError(entry=value, domain=self.domain, min_length=12)

        return value.title()


    def validate_staff_email(self, value:str):# Add more constraints
        value = (value or "").strip()
        if not value:
            raise EmptyFieldError(entry=value, domain=self.domain)
        if len(value.strip()) < 12:
            raise TextTooShortError(entry=value, domain=self.domain, min_length=12)

        return value.lower()


    def validate_email_address(self, value:str):# Add more constraints
        value = (value or "").strip()
        if not value:
            raise EmptyFieldError(entry=value, domain=self.domain)
            #raise EmailFormatError()
        return value


    @staticmethod
    def validate_phone(value: str) -> str:
        cleaned_number = re.sub(r'[\s\-\(\)]', '', value.strip())
        e164_pattern = re.compile(r'^\+\d{1,3}\d{11,15}$')

        if e164_pattern.match(cleaned_number):
            return cleaned_number
        else:
            raise InvalidPhoneError(entry=value)


    def validate_date(self, value: date) -> date:
        """Validate that date is not in the future."""
        if value > date.today():
            raise FutureDateError(entry=value, domain = self.domain)
        return value


    @staticmethod
    def validate_session_start_year(value):
        current_year = datetime.now().year
        if value < current_year or value > current_year + 1:
            raise InvalidSessionYearError(entry=value, current_year=current_year)

        return value

