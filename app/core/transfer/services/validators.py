from app.core.shared.exceptions import (
    EmptyFieldError, TextTooShortError, InvalidCharacterError, TextTooLongError,
)
from datetime import datetime
import re

from app.core.shared.exceptions.entry_validation_errors import PastYearError, SessionYearFormatError, \
    FutureYearError, InvalidSessionRangeError


class TransferValidator:
    def __init__(self):
        self.domain = "TRANSFER"

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




