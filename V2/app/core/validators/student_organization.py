
from ...core.errors.input_validation_errors import (
    EmptyFieldError, BlankFieldError, TextTooShortError, InvalidCharacterError,InvalidCodeError
)

class StudentOrganizationValidator:
    def __init__(self):
        self.domain = "STUDENT ORGANIZATION"

    def validate_name(self, value:str) -> str:
        if not value:
            raise EmptyFieldError(entry = value, domain = self.domain)
        if not value.strip():
            raise BlankFieldError(entry = value, domain = self.domain)
        if len(value.strip()) < 3:
            raise TextTooShortError(entry = value, domain = self.domain, min_length = 3)
        if any(val.isnumeric() for val in value):
            raise InvalidCharacterError(entry=value, domain=self.domain)

        return value.strip().title()

    def validate_level_name(self, value:str) -> str:
        if not value:
            raise EmptyFieldError(entry = value, domain = self.domain)
        if not value.strip():
            raise BlankFieldError(entry = value, domain = self.domain)
        if len(value.strip()) < 3:
            raise TextTooShortError(entry = value, domain = self.domain, min_length = 3)

        return value.strip().upper()

    def validate_description(self, value:str):
        if not value:
            raise EmptyFieldError(entry = value, domain = self.domain)
        if not value.strip():
            raise BlankFieldError(entry = value, domain = self.domain)
        if len(value.strip()) < 3:
            raise TextTooShortError(entry=value, domain=self.domain, min_length=3)

        return value.strip().capitalize()


    def validate_code(self, value: str) -> str:
        if not value:
            raise EmptyFieldError(entry = value, domain = self.domain)
        if not value.strip():
            raise BlankFieldError(entry = value, domain = self.domain)
        if len(value.strip()) != 3:
            raise InvalidCodeError(entry = value, length=3, domain = self.domain)
        if any(val.isnumeric() for val in value):
            raise InvalidCharacterError(entry = value, domain = self.domain)

        return value.strip().upper()

