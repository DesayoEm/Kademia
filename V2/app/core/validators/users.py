from datetime import date, datetime
import re
from pydantic import EmailStr, ValidationError
from ..errors.input_validation_errors import InvalidSessionYearError, EmailFormatError
from ...core.errors.input_validation_errors import(
    BlankFieldError, DateError, TextTooShortError,EmptyFieldError, InvalidCharacterError, InvalidPhoneError
    )
class UserValidator:
    def __init__(self):
        self.domain = "USER PROFILE"

    def validate_name(self, value:str):
        if not value:
            raise EmptyFieldError(entry = value, domain = self.domain)
        if not value.strip():
            raise BlankFieldError(entry = value, domain = self.domain)
        if len(value.strip()) < 2:
            raise TextTooShortError(entry = value, domain = self.domain, min_length = 2)
        if any(val.isnumeric() for val in value):
            raise InvalidCharacterError(entry=value, domain=self.domain)

        return value.title()


    def validate_address(self, value:str):
        if not value:
            raise EmptyFieldError(entry=value, domain=self.domain)
        if not value.strip():
            raise BlankFieldError(entry=value, domain=self.domain)
        if len(value.strip()) < 12:
            raise TextTooShortError(entry=value, domain=self.domain, min_length=12)

        return value.title()


    def validate_staff_email(self, value:str):# FIX. Add more constraints
        if not value:
            raise EmptyFieldError(entry=value, domain=self.domain)
        if not value.strip():
            raise BlankFieldError(entry=value, domain=self.domain)
        if len(value.strip()) < 12:
            raise TextTooShortError(entry=value, domain=self.domain, min_length=12)

        return value.lower()

    def validate_email_address(self, value:str):
        if not value:
            raise EmptyFieldError(entry=value, domain=self.domain)
        if not value.strip():
            raise BlankFieldError(entry=value, domain=self.domain)
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


    def validate_date(self, date_input: date) -> date:
        """Validate that date is not in the future."""
        if date_input > date.today():
            raise DateError(date_input=date_input, domain = self.domain)
        return date_input

    @staticmethod
    def validate_session_start_year(value):
        current_year = datetime.now().year
        if value < current_year or value > current_year + 1:
            raise InvalidSessionYearError(entry=value, current_year=current_year)

        return value

