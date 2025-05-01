from V2.app.core.shared.exceptions.student_organisation_errors import InvalidCodeError
from V2.app.core.shared.exceptions.entry_validation_errors import (
    EmptyFieldError, TextTooShortError, InvalidCharacterError, InvalidOrderNumberError,
    TextTooLongError
)

class CurriculumValidator:
    def __init__(self):
        self.domain = "CURRICULUM"

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


