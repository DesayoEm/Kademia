from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.academic_structure.models.academic_structure import AcademicLevel
from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.academic_structure.factories.academic_level import AcademicLevelFactory
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.academic_structure.schemas.academic_level import (
    AcademicLevelCreate, AcademicLevelUpdate, AcademicLevelResponse, AcademicLevelFilterParams
)


class AcademicLevelCrud:
    """CRUD operations for academic levels."""

    def __init__(self, session: Session, current_user = None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.current_user = current_user
        self.factory = AcademicLevelFactory(session, current_user=current_user)
        self.export_service = ExportService(session)


    def create_level(self, data: AcademicLevelCreate) -> AcademicLevelResponse:
        """Create a new academic level."""
        level = self.factory.create_academic_level(data)
        return AcademicLevelResponse.model_validate(level)


    def get_level(self, level_id: UUID) -> AcademicLevelResponse:
        """Get academic level by ID."""
        level = self.factory.get_academic_level(level_id)
        return AcademicLevelResponse.model_validate(level)


    def get_all_levels(self, filters: AcademicLevelFilterParams) -> List[AcademicLevelResponse]:
        """Get all active academic levels."""
        levels = self.factory.get_all_academic_levels(filters)
        return [AcademicLevelResponse.model_validate(level) for level in levels]


    def update_level(self, level_id: UUID, data: AcademicLevelUpdate) -> AcademicLevelResponse:
        """Update academic level information."""
        data = data.model_dump(exclude_unset=True)
        updated_level = self.factory.update_academic_level(level_id, data)
        return AcademicLevelResponse.model_validate(updated_level)


    def archive_level(self, level_id: UUID, reason: ArchiveReason) -> None:
        """Archive an academic level.
        Args:
            level_id: academic level UUID
            reason: Reason for archiving
        Returns:
            AcademicLevelResponse: Archived academic level
        """
        self.factory.archive_academic_level(level_id, reason)


    def export_level(self, level_id: UUID, export_format: str) -> str:
        """Export level and its associated data
        Args:
            level_id: level UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            AcademicLevel, level_id, export_format
        )


    def delete_level(self, level_id: UUID) -> None:
        """Permanently delete a academic level."""
        self.factory.delete_academic_level(level_id)


    # Archived AcademicLevel operations
    def get_archived_level(self, level_id: UUID) -> AcademicLevelResponse:
        """Get an archived academic level by ID."""
        level = self.factory.get_archived_academic_level(level_id)
        return AcademicLevelResponse.model_validate(level)


    def get_all_archived_levels(self, filters: AcademicLevelFilterParams) -> List[AcademicLevelResponse]:
        """Get all archived academic levels."""
        levels = self.factory.get_all_archived_academic_levels(filters)
        return [AcademicLevelResponse.model_validate(level) for level in levels]


    def restore_level(self, level_id: UUID) -> AcademicLevelResponse:
        """Restore an archived academic level."""
        level = self.factory.restore_academic_level(level_id)
        return AcademicLevelResponse.model_validate(level)


    def delete_archived_level(self, level_id: UUID) -> None:
        """Permanently delete an archived academic level."""
        self.factory.delete_archived_academic_level(level_id)