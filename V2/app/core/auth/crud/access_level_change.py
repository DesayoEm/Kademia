from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from V2.app.core.auth.models.auth import AccessLevelChange
from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.auth.schemas.access_level_change import (
    AccessLevelFilterParams, AccessLevelChangeCreate, AccessLevelChangeResponse
)
from V2.app.core.auth.factories.access_level_factory import AccessLevelChangeFactory
from V2.app.core.shared.services.export_service.export import ExportService


class AccessLevelChangeCrud:
    """CRUD operations for access level changes."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
        """
        self.session = session
        self.factory = AccessLevelChangeFactory(session)
        self.export_service = ExportService(session)


    def create_access_level_change(self, staff_id: UUID, data: AccessLevelChangeCreate) -> AccessLevelChangeResponse:
        """Create a new level change .
        Args:
            staff_id: ID of staff to change access level for
            data: Validated level change  creation data
        Returns:
            AccessLevelChangeResponse: Created level change 
        """
        level_change = self.factory.create_level_change(staff_id, data)
        return AccessLevelChangeResponse.model_validate(level_change)


    def get_access_level_change(self, level_change_id: UUID) -> AccessLevelChangeResponse:
        """Get level change by ID.
        Args:
            level_change_id: level change  UUID
        Returns:
            AccessLevelChangeResponse: Retrieved level change 
        """
        level_change = self.factory.get_level_change(level_change_id)
        return AccessLevelChangeResponse.model_validate(level_change)


    def get_all_access_level_changes(self, filters: AccessLevelFilterParams) -> List[AccessLevelChangeResponse]:
        """Get all active level changes.
        Returns:
            List[AccessLevelChangeResponse]: List of active level changes
        """
        level_changes = self.factory.get_all_level_changes(filters)
        return [AccessLevelChangeResponse.model_validate(level_change) for level_change  in level_changes]


    def archive_access_level_change(self, level_change_id: UUID, reason: ArchiveReason) -> None:
        """Archive a level change .
        Args:
            level_change_id: level change  UUID
            reason: Reason for archiving
        Returns:
            AccessLevelChangeResponse: Archived level change 
        """
        self.factory.archive_level_change(level_change_id, reason)


    def export_access_level_change(self, level_change_id: UUID, export_format: str) -> str:
        """Export level change  and its associated data
        Args:
            level_change_id: level change  UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            AccessLevelChange, level_change_id, export_format
        )


    def delete_access_level_change(self, level_change_id: UUID) -> None:
        """Permanently delete a level change .
        Args:
            level_change_id: level change  UUID
        """
        self.factory.delete_level_change(level_change_id)


    # Archived level change  operations
    def get_archived_access_level_change(self, level_change_id: UUID) -> AccessLevelChangeResponse:
        """Get an archived level change  by ID.
        Args:
            level_change_id: level change  UUID
        Returns:
            AccessLevelChangeResponse: Retrieved archived level change 
        """
        level_change = self.factory.get_archived_level_change(level_change_id)
        return AccessLevelChangeResponse.model_validate(level_change)

    def get_all_archived_access_level_changes(self, filters: AccessLevelFilterParams) -> List[AccessLevelChangeResponse]:
        """Get all archived level change s.
        Args:
            filters: Filter parameters
        Returns:
            List[AccessLevelChangeResponse]: List of archived level change s
        """
        level_changes = self.factory.get_all_archived_level_changes(filters)
        return [AccessLevelChangeResponse.model_validate(level_change) for level_change  in level_changes]


    def restore_access_level_change(self, level_change_id: UUID) -> AccessLevelChangeResponse:
        """Restore an archived level change .
        Args:
            level_change_id: level change  UUID
        Returns:
            AccessLevelChangeResponse: Restored level change 
        """
        level_change = self.factory.restore_level_change(level_change_id)
        return AccessLevelChangeResponse.model_validate(level_change)


    def delete_archived_access_level_change(self, level_change_id: UUID) -> None:
        """Permanently delete an archived level change .
        Args:
            level_change_id: level change  UUID
        """
        self.factory.delete_archived_level_change(level_change_id)