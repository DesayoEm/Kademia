from V2.app.core.shared.errors import LifetimeValidityConflictError, TemporaryValidityConflictError
from V2.app.core.shared.errors.entry_validation_errors import PastDateError, TextTooLongError
from V2.app.core.shared.errors import (
    EmptyFieldError, InvalidCharacterError, TextTooShortError
)
from datetime import datetime, date
from dateutil.parser import parse


class StaffManagementValidator:
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

    def parse_validity_date(self, value: str) -> date:
        """convert date string to a date object"""
        try:
            return parse(value).date()

        except ValueError:
                raise TemporaryValidityConflictError(entry = value, domain = self.domain)


    def validate_valid_until(self, validity_type: str, value:str) -> str:
        """Create a valid until date depending on input"""

        if validity_type.lower() == 'lifetime':
            if value.lower().strip() != 'lifetime':
                raise LifetimeValidityConflictError(entry = value)
            return value.title()


        elif validity_type.lower() == 'temporary':
            converted_str = self.parse_validity_date(value)
            return str(self.validate_valid_until_date(converted_str))


















