from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.identity.models.guardian import Guardian
from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.identity.factories.guardian import GuardianFactory
from V2.app.core.identity.schemas.guardian import (
    GuardianCreate, GuardianUpdate, GuardianResponse, GuardianFilterParams
)

class GuardianCrud:
    """CRUD operations for guardian."""

    def __init__(self, session: Session, current_user = None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.current_user = current_user
        self.factory = GuardianFactory(session, current_user=current_user)
        self.export_service = ExportService(session)


    def create_guardian(self, data: GuardianCreate) -> GuardianResponse:
        """Create a new guardian."""
        guardian = self.factory.create_guardian(data)
        return GuardianResponse.model_validate(guardian)


    def get_guardian(self, guardian_id: UUID) -> GuardianResponse:
        """Get guardian by ID."""
        guardian = self.factory.get_guardian(guardian_id)
        return GuardianResponse.model_validate(guardian)


    def get_all_guardians(self, filters: GuardianFilterParams) -> List[GuardianResponse]:
        """Get all active guardians."""
        guardians = self.factory.get_all_guardians(filters)
        return [GuardianResponse.model_validate(guardian) for guardian in guardians]


    def update_guardian(self, guardian_id: UUID, data: GuardianUpdate) -> GuardianResponse:
        """Update guardian information."""
        data = data.model_dump()
        updated_guardian = self.factory.update_guardian(guardian_id, data)
        return GuardianResponse.model_validate(updated_guardian)


    def archive_guardian(self, guardian_id: UUID, reason: ArchiveReason) -> None:
        """Archive a guardian.
        Args:
            guardian_id: guardian UUID
            reason: Reason for archiving
        Returns:
            GuardianResponse: Archived guardian
        """
        self.factory.archive_guardian(guardian_id, reason)


    def export_guardian(self, guardian_id: UUID, export_format: str) -> str:
        """Export guardian and its associated data
        Args:
            guardian_id: guardian UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Guardian, guardian_id, export_format
        )

    def delete_guardian(self, guardian_id: UUID) -> None:
        """Permanently delete a guardian."""
        self.factory.delete_guardian(guardian_id)


    # Archived guardian operations
    def get_archived_guardian(self, guardian_id: UUID) -> GuardianResponse:
        """Get an archived guardian by ID."""
        guardian = self.factory.get_archived_guardian(guardian_id)
        return GuardianResponse.model_validate(guardian)


    def get_all_archived_guardians(self, filters: GuardianFilterParams) -> List[GuardianResponse]:
        """Get all archived guardians."""
        guardians = self.factory.get_all_archived_guardians(filters)
        return [GuardianResponse.model_validate(guardian) for guardian in guardians]


    def restore_guardian(self, guardian_id: UUID) -> GuardianResponse:
        """Restore an archived guardian."""
        guardian = self.factory.restore_guardian(guardian_id)
        return GuardianResponse.model_validate(guardian)


    def delete_archived_guardian(self, guardian_id: UUID) -> None:
        """Permanently delete an archived guardian."""
        self.factory.delete_archived_guardian(guardian_id)