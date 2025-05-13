from V2.app.core.shared.exceptions import InvalidRankNumberError
from V2.app.core.shared.exceptions.academic_structure_errors import InvalidCodeError
from V2.app.core.shared.exceptions.entry_validation_errors import (
    EmptyFieldError, TextTooShortError, InvalidCharacterError, InvalidOrderNumberError,
    TextTooLongError
)
from V2.app.core.shared.exceptions.progression_errors import InvalidPromotionLevelError


class ProgressionValidator:
    def __init__(self):
        self.domain = "PROGRESSION"

    @staticmethod
    def validate_promotion_level(previous_level, next_level):
        if previous_level.promotion_rank != next_level.promotion_rank +1:
            raise InvalidPromotionLevelError(
                next_level_id=next_level.id,
                previous_level_id=previous_level.id
            )

        return next_level

    @staticmethod
    def validate_repetition_level(previous_level, next_level):
        if not next_level.promotion_rank < previous_level.promotion_rank:
            raise InvalidPromotionLevelError(next_level_id=next_level, previous_level_id=previous_level)

        return next_level