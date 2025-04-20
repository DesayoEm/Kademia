from V2.app.core.shared.errors.student_organisation_errors import InvalidCodeError
from ...core.errors.entry_validation_errors import (
    EmptyFieldError, TextTooShortError, InvalidCharacterError, InvalidOrderNumberError,
    TextTooLongError
)

class AcademicStructureValidator:
    def __init__(self):
        self.domain = "ACADEMIC STRUCTURE"

    def validate_name(self, value:str) -> str:
        value = (value or "").strip()
        if not value:
            raise EmptyFieldError(entry=value, domain=self.domain)
        if len(value.strip()) < 3:
            raise TextTooShortError(entry = value, domain = self.domain, min_length = 3)
        if len(value.strip()) > 100:
            raise TextTooLongError(entry=value, max_length=100, domain=self.domain)
        if any(val.isnumeric() for val in value):
            raise InvalidCharacterError(entry=value, domain=self.domain)

        return value.strip().title()


    def validate_description(self, value:str):
        value = (value or "").strip()
        if not value:
            raise EmptyFieldError(entry=value, domain=self.domain)
        if len(value.strip()) < 3:
            raise TextTooShortError(entry=value, domain=self.domain, min_length=3)
        if len(value.strip()) > 500:
            raise TextTooLongError(entry=value, max_length=500, domain=self.domain)

        return value.strip().capitalize()


    def validate_level_name(self, value:str) -> str:
        value = (value or "").strip()
        if not value:
            raise EmptyFieldError(entry=value, domain=self.domain)
        if len(value.strip()) < 3:
            raise TextTooShortError(entry = value, domain = self.domain, min_length = 3)

        return value.strip().upper()


    @staticmethod
    def validate_order(order:int) -> int:
        if order <= 0:
            raise InvalidOrderNumberError(entry=order)

        return order


    def validate_code(self, value: str) -> str:
        value = (value or "").strip()
        if not value:
            raise EmptyFieldError(entry=value, domain=self.domain)
        if len(value.strip()) != 3:
            raise InvalidCodeError(entry = value, length=3, domain = self.domain)
        if any(val.isnumeric() for val in value):
            raise InvalidCharacterError(entry = value, domain = self.domain)

        return value.strip().upper()

