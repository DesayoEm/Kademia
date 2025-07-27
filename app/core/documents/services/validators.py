from app.core.shared.exceptions import (
    EmptyFieldError, TextTooShortError, InvalidCharacterError, TextTooLongError,
)
from datetime import datetime
import re

from app.core.shared.exceptions.entry_validation_errors import PastYearError, SessionYearFormatError, \
    FutureYearError, InvalidSessionRangeError


class DocumentValidator:
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

    def validate_academic_session(self, value):
        match = re.fullmatch(r"(\d{4})/(\d{4})", value)
        if not match:
            raise SessionYearFormatError(entry=value, domain=self.domain)

        first_year, second_year = map(int, match.groups())
        current_year = datetime.now().year

        if first_year > current_year:
            raise FutureYearError(entry=value, domain=self.domain)

        if second_year != first_year + 1:
            raise InvalidSessionRangeError(entry=value, domain=self.domain)

        return value


    def validate_current_academic_session(self, value):
        match = re.fullmatch(r"(\d{4})/(\d{4})", value)
        if not match:
            raise SessionYearFormatError(entry=value, domain=self.domain)

        first_year, second_year = map(int, match.groups())
        current_year = datetime.now().year

        if first_year < current_year:
            raise PastYearError(entry=value, domain=self.domain)

        if first_year > current_year:
            raise FutureYearError(entry=value, domain=self.domain)

        if second_year != first_year + 1:
            raise InvalidSessionRangeError(entry=value, domain=self.domain)

        return value




