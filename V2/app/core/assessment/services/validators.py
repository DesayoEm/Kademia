from uuid import UUID
from datetime import datetime, date
from sqlalchemy import select, func
import re
from sqlalchemy.orm import Session
from V2.app.core.shared.exceptions import (
    FutureDateError, MaxScoreTooHighError, ScoreExceedsMaxError,
    PastYearError, SessionYearFormatError, FutureYearError, InvalidSessionRangeError
)


class AssessmentValidator:
    """Validates fields related to grading and assessment."""

    def __init__(self, session: Session):
        self.session = session


    @staticmethod
    def validate_graded_date(value: date) -> date:
        """Ensure graded date is not in the future."""
        current = date.today()
        if value > current:
            raise FutureDateError(entry=value)
        return value

    @staticmethod
    def validate_max_score(value: int) -> int:
        """Ensure max score is within allowed bounds."""
        if value > 100:
            raise MaxScoreTooHighError(entry=value)
        return value

    @staticmethod
    def validate_score(max_score: int, value: int) -> int:
        """Ensure score doesn't exceed max score."""
        if value > max_score:
            raise ScoreExceedsMaxError(entry=value, max_score=max_score)
        return value

    @staticmethod
    def validate_academic_session(value: str) -> str:
        """Ensure session year is current and well-formatted."""
        match = re.fullmatch(r"(\d{4})/(\d{4})", value)
        if not match:
            raise SessionYearFormatError(entry=value)

        first_year, second_year = map(int, match.groups())
        current_year = datetime.now().year

        if first_year < current_year:
            raise PastYearError(entry=value)
        if first_year > current_year:
            raise FutureYearError(entry=value)
        if second_year != first_year + 1:
            raise InvalidSessionRangeError(entry=value)

        return value
