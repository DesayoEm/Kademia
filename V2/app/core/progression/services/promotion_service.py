from sqlalchemy.orm import Session
from uuid import UUID
from V2.app.core.academic_structure.factories.academic_level import AcademicLevelFactory
from V2.app.core.academic_structure.models import AcademicLevel
from V2.app.core.progression.models.progression import Repetition
from V2.app.core.shared.exceptions import InvalidRepetitionLevelError
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.shared.exceptions.progression_errors import InvalidPromotionLevelError


class ProgressionService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user
        self.export_service = ExportService(session)
        self.domain = "PROGRESSION"

    @staticmethod
    def validate_promotion_level(previous_level, next_level):
        if previous_level.promotion_rank != next_level.promotion_rank + 1:
            raise InvalidPromotionLevelError(
                next_level_id=next_level.id,
                previous_level_id=previous_level.id
            )

        return next_level

    def validate_repetition_level(self, failed_level_id, repeat_level_id):

        academic_factory = AcademicLevelFactory(self.session, AcademicLevel, self.current_user)
        failed_level = academic_factory.get_academic_level(failed_level_id)
        repeat_level = academic_factory.get_academic_level(repeat_level_id)

        if not repeat_level.promotion_rank <= failed_level.promotion_rank:
            raise InvalidRepetitionLevelError(
                repeat_level_id=repeat_level_id, failed_level_id=failed_level_id
            )

        return repeat_level

    def export_guardian(self, repetition_id: UUID, export_format: str) -> str:
        """Export repetition object and its associated data
        Args:
            repetition_id: Guardian UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Repetition, repetition_id, export_format
        )