from ..errors.input_validation_errors import InvalidValidityYearError, InvalidYearError, InvalidYearLengthError, \
    PastDateError
from ...core.errors.input_validation_errors import (
    EmptyFieldError, BlankFieldError, InvalidCharacterError, TextTooShortError
)
from datetime import datetime, date


class StaffOrganizationValidator:
    def _init__(self):
        self.domain = "STAFF ORGANIZATION"

    @staticmethod
    def validate_name(value:str) -> str:
        if not value:
            raise BlankFieldError(entry = value)
        if not value.strip():
            raise BlankFieldError(entry = value)
        if len(value.strip()) < 3:
            raise TextTooShortError(entry = value, min_length = 3)
        if any(val.isnumeric() for val in value):
            raise InvalidCharacterError(entry=value)
        
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


    @staticmethod
    def validate_valid_until_date(value: date) -> date:

        current_date = datetime.today().date()
        if value < current_date:
            raise PastDateError(entry=value)

        return value

















