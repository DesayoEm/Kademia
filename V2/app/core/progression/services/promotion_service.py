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


    def export_promotion_audit(self, promotion_id: UUID, export_format: str) -> str:
        """Export promotion object and its associated data
        Args:
            promotion_id: Promotion UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Repetition, promotion_id, export_format
        )