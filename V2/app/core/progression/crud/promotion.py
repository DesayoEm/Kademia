from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.progression.models.progression import Promotion
from V2.app.core.progression.schemas.promotion import (
    StudentPromotionCreate,
    StudentPromotionResponse,
    PromotionFilterParams
)
from V2.app.core.progression.factories.promotion import PromotionFactory
from V2.app.core.shared.schemas.enums import ArchiveReason


class PromotionCrud:
    """CRUD operations for student promotions."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
        """
        self.session = session
        self.factory = PromotionFactory(session)

    def create_promotion(self, student_id: UUID, data: StudentPromotionCreate) -> StudentPromotionResponse:
        """Create a new promotion record for a student."""
        promotion = self.factory.create_promotion(student_id, data)
        return StudentPromotionResponse.model_validate(promotion)

    def get_promotion(self, promotion_id: UUID) -> StudentPromotionResponse:
        """Get a specific promotion record by ID."""
        promotion = self.factory.get_promotion(promotion_id)
        return StudentPromotionResponse.model_validate(promotion)

    def get_all_promotions(self, filters: PromotionFilterParams) -> List[StudentPromotionResponse]:
        """Get all active promotion records."""
        promotions = self.factory.get_all_promotions(filters)
        return [StudentPromotionResponse.model_validate(promo) for promo in promotions]

    def update_promotion(self, promotion_id: UUID, data: dict) -> StudentPromotionResponse:
        """Update an existing promotion record."""
        updated = self.factory.update_promotion(promotion_id, data.model_dump(exclude_unset=True))
        return StudentPromotionResponse.model_validate(updated)

    def archive_promotion(self, promotion_id: UUID, reason: ArchiveReason) -> None:
        """Archive a promotion record."""
        self.factory.archive_promotion(promotion_id, reason)

    def delete_promotion(self, promotion_id: UUID) -> None:
        """Permanently delete a promotion record."""
        self.factory.delete_promotion(promotion_id)

    def get_archived_promotion(self, promotion_id: UUID) -> StudentPromotionResponse:
        """Get an archived promotion record by ID."""
        archived = self.factory.get_archived_promotion(promotion_id)
        return StudentPromotionResponse.model_validate(archived)

    def get_all_archived_promotions(self, filters: PromotionFilterParams) -> List[StudentPromotionResponse]:
        """Get all archived promotion records."""
        promotions = self.factory.get_all_archived_promotions(filters)
        return [StudentPromotionResponse.model_validate(promo) for promo in promotions]

    def restore_promotion(self, promotion_id: UUID) -> StudentPromotionResponse:
        """Restore an archived promotion record."""
        restored = self.factory.restore_promotion(promotion_id)
        return StudentPromotionResponse.model_validate(restored)

    def delete_archived_promotion(self, promotion_id: UUID) -> None:
        """Permanently delete an archived promotion record."""
        self.factory.delete_archived_promotion(promotion_id)
