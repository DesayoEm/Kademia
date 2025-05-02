from V2.app.core.shared.exceptions import (
    FutureDateError, MaxScoreTooHighError, ScoreExceedsMaxError, InvalidWeightError
)
from datetime import datetime, date
import re

from V2.app.core.shared.exceptions.entry_validation_errors import PastYearError, SessionYearFormatError, \
    FutureYearError, InvalidSessionRangeError


class AssessmentValidator:
    def __init__(self):
        self.domain = "Assessment"

    def validate_graded_date(self, value:date) -> date:
        current = date.today()
        if value > current:
            raise FutureDateError(entry=value, domain=self.domain)
        return value

    def validate_max_score(self, value:int) -> int:
        if value > 100:
            raise MaxScoreTooHighError(entry=value, domain=self.domain)
        return value


    def validate_score(self,max_score: int, value:int) -> int:
        if value > max_score:
            raise ScoreExceedsMaxError(entry=value,max_score=max_score, domain=self.domain)
        return value

    def validate_weight(self, value: int) -> int:
        cumulative = 0 #query later
        if value + cumulative > 100:
            raise InvalidWeightError(
                entry=value, cumulative_weight=cumulative, domain=self.domain
            )
        return value

    def validate_session_year(self, value):
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



