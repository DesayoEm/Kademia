from datetime import date
import re
from ...core.errors.profile_errors import TextTooShortError, DateError


class UserValidators:

    @staticmethod
    def validate_name(value: str):
        if len(value.strip()) < 2:
            raise TextTooShortError(data = value, min_length=2)
        return value.title()

    @staticmethod
    def validate_address(value: str):
        if len(value.strip()) < 10:
            raise TextTooShortError(data = value, min_length=10)
        return value.title()

    @staticmethod
    def validate_staff_email(value: str):
        if len(value.strip()) < 10:
            raise TextTooShortError
        return value.title()

    @staticmethod
    def validate_phone(value: str): #FIX
        if len(value.strip()) < 10:
            raise TextTooShortError
        return value.title()

    @staticmethod
    def validate_date(date_input: date) -> date:
        """Validate that date is not in the future."""
        if date_input > date.today():
            raise DateError
        return date_input