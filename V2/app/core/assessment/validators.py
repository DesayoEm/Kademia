from uuid import UUID
from datetime import datetime, date
from sqlalchemy import select, func
import re

from sqlalchemy.orm import Session

from V2.app.core.assessment.models.assessment import Grade
from V2.app.core.shared.exceptions import (
    FutureDateError, MaxScoreTooHighError, ScoreExceedsMaxError, InvalidWeightError,
    PastYearError, SessionYearFormatError, FutureYearError, InvalidSessionRangeError
)
from V2.app.core.shared.schemas.enums import Term

class AssessmentValidator:
    """Validates fields related to grading and assessment."""

    def __init__(self, session: Session):
        self.domain = "Assessment"
        self.session = session

    def validate_weight(self, value: int, student_id: UUID, subject_id: UUID,
                        academic_session: str, term: Term) -> int:
        """Ensure cumulative weight for a term doesn't exceed 100."""
        stmt = select(func.coalesce(func.sum(Grade.weight), 0)).where(
            Grade.student_id == student_id,
            Grade.subject_id == subject_id,
            Grade.academic_session == academic_session,
            Grade.term == term,
        )
        cumulative = self.session.scalar(stmt)

        if value + cumulative > 100:
            raise InvalidWeightError(
                entry=value, cumulative_weight=cumulative, domain=self.domain
            )
        return value

    def validate_graded_date(self, value: date) -> date:
        """Ensure graded date is not in the future."""
        current = date.today()
        if value > current:
            raise FutureDateError(entry=value, domain=self.domain)
        return value

    def validate_max_score(self, value: int) -> int:
        """Ensure max score is within allowed bounds."""
        if value > 100:
            raise MaxScoreTooHighError(entry=value, domain=self.domain)
        return value

    def validate_score(self, max_score: int, value: int) -> int:
        """Ensure score doesn't exceed max score."""
        if value > max_score:
            raise ScoreExceedsMaxError(entry=value, max_score=max_score, domain=self.domain)
        return value

    def validate_academic_session(self, value: str) -> str:
        """Ensure session year is current and well-formatted."""
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
