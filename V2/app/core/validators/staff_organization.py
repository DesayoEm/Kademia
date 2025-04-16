from ..errors.entry_validation_errors import InvalidYearError, InvalidYearLengthError, \
    PastDateError, TextTooLongError
from ...core.errors.entry_validation_errors import (
    EmptyFieldError, InvalidCharacterError, TextTooShortError
)
from datetime import datetime, date


class StaffOrganizationValidator:
    def __init__(self):
        self.domain = "STAFF ORGANIZATION"


    def validate_name(self, value:str) -> str:
        value = (value or "").strip()
        if not value:
            raise EmptyFieldError(entry=value, domain = self.domain)
        if len(value.strip()) < 3:
            raise TextTooShortError(entry = value, min_length = 3, domain = self.domain)
        if len(value.strip()) > 100:
            raise TextTooLongError(entry = value, max_length = 100, domain = self.domain)
        if any(val.isnumeric() for val in value):
            raise InvalidCharacterError(entry=value, domain = self.domain)
        
        return value.strip().title()


    def validate_description(self, value: str) -> str:
        value = (value or "").strip()
        if not value:
            raise EmptyFieldError(entry=value, domain = self.domain)
        if len(value.strip()) < 3:
            raise TextTooShortError(entry=value, min_length=3, domain = self.domain)
        if len(value.strip()) > 500:
            raise TextTooLongError(entry=value, max_length=500, domain=self.domain)

        return value.strip().capitalize()


    def validate_valid_until_date(self, value: date) -> date:

        current_date = datetime.today().date()
        if value < current_date:
            raise PastDateError(entry=value, domain = self.domain)

        return value

















