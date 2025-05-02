from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.documents.models.documents import StudentAward
from V2.app.core.documents.factories.award_factory import AwardFactory
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.documents.schemas.student_award import (
    AwardCreate, AwardFilterParams, AwardUpdate, AwardResponse
)


class AwardCrud:
    """CRUD operations for awards."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
        """
        self.session = session
        self.factory = AwardFactory(session)
        self.export_service = ExportService(session)


    def create_award(self, data: AwardCreate) -> AwardResponse:
        """Create a new award.
        Args:
            data: Validated award creation data
        Returns:
            AwardResponse: Created award
        """
        new_award = self.factory.create_award(data)
        return AwardResponse.model_validate(new_award)


    def get_award(self, award_id: UUID) -> AwardResponse:
        """Get award by ID.
        Args:
            award_id: award UUID
        Returns:
            AwardResponse: Retrieved award
        """
        award_response = self.factory.get_award(award_id)
        return AwardResponse.model_validate(award_response)


    def get_all_awards(self, filters: AwardFilterParams) -> List[AwardResponse]:
        """Get all active awards.
        Returns:
            List[AwardResponse]: List of active awards
        """
        awards = self.factory.get_all_awards(filters)
        return [AwardResponse.model_validate(award) for award in awards]


    def update_award(self, award_id: UUID, data: AwardUpdate) -> AwardResponse:
        """Update award information.
        Args:
            award_id: award UUID
            data: Validated update data
        Returns:
            AwardResponse: Updated award
        """
        data = data.model_dump(exclude_unset=True)
        updated_award = self.factory.update_award(award_id, data)
        return AwardResponse.model_validate(updated_award)

    def archive_award(self, award_id: UUID, reason: ArchiveReason) -> None:
        """Archive a award.
        Args:
            award_id: award UUID
            reason: Reason for archiving
        Returns:
            AwardResponse: Archived award
        """
        self.factory.archive_award(award_id, reason)

    def export_award(self, award_id: UUID, export_format: str) -> str:
        """Export award and its associated data
        Args:
            award_id: award UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            StudentAward, award_id, export_format
        )


    def delete_award(self, award_id: UUID) -> None:
        """Permanently delete a award.
        Args:
            award_id: award UUID
        """
        self.factory.delete_award(award_id)


    # Archived award operations
    def get_archived_award(self, award_id: UUID) -> AwardResponse:
        """Get an archived award by ID.
        Args:
            award_id: award UUID
        Returns:
            AwardResponse: Retrieved archived award
        """
        award_response = self.factory.get_archived_award(award_id)
        return AwardResponse.model_validate(award_response)

    def get_all_archived_awards(self, filters: AwardFilterParams) -> List[AwardResponse]:
        """Get all archived awards.
        Args:
            filters: Filter parameters
        Returns:
            List[AwardResponse]: List of archived awards
        """
        awards = self.factory.get_all_archived_awards(filters)
        return [AwardResponse.model_validate(award) for award in awards]


    def restore_award(self, award_id: UUID) -> AwardResponse:
        """Restore an archived award.
        Args:
            award_id: award UUID
        Returns:
            AwardResponse: Restored award
        """
        restored_award = self.factory.restore_award(award_id)
        return AwardResponse.model_validate(restored_award)


    def delete_archived_award(self, award_id: UUID) -> None:
        """Permanently delete an archived award.
        Args:
            award_id: award UUID
        """
        self.factory.delete_archived_award(award_id)