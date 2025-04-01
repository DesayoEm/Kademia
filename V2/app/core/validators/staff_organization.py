from ..errors.input_validation_errors import InvalidValidityYearError, InvalidYearError, InvalidYearLengthError
from ...core.errors.input_validation_errors import (
    EmptyFieldError, BlankFieldError, InvalidCharacterError, TextTooShortError
)
from datetime import datetime


class StaffOrganizationValidator:
    def _init__(self):
        self.domain = "STAFF ORGANIZATION"

    def validate_name(self, value:str) -> str:
        if not value:
            raise BlankFieldError(entry = value, domain = self.domain)
        if not value.strip():
            raise BlankFieldError(entry = value, domain = self.domain)
        if len(value.strip()) < 3:
            raise TextTooShortError(entry = value, domain = self.domain, min_length = 3)
        if any(val.isnumeric() for val in value):
            raise InvalidCharacterError(entry=value, domain=self.domain)
        
        return value.strip().title()


    def validate_description(self, value:str):
        if not value:
            raise EmptyFieldError(entry = value, domain = self.domain)
        if not value.strip():
            raise BlankFieldError(entry = value, domain = self.domain)

        return value.strip().capitalize()


    def validate_valid_until_year(self, value: str) -> str:
        value = value.strip()

        if len(value) != 4:
            raise InvalidYearLengthError(year=value, domain = self.domain)

        if not value.isdigit():
            raise InvalidYearError(year = value, domain = self.domain)

        year = int(value)
        current_year = datetime.now().year
        if year < current_year:
            raise InvalidValidityYearError(year = year)

        return str(year)
















