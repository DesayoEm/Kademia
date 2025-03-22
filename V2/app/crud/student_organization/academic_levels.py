from ...database.models.enums import ArchiveReason
from ...schemas.student_organization.academic_level import (
    AcademicLevelCreate, AcademicLevelUpdate, AcademicLevelResponse, AcademicLevelFilterParams
)
from ...core.factories.student_organization.academic_level import AcademicLevelFactory
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List


class AcademicLevelCrud:
    """CRUD operations for academic levels."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        self.factory = AcademicLevelFactory(session)


    def create_level(self, data: AcademicLevelCreate) -> AcademicLevelResponse:
        """Create a new academic level.
        Args:
            data: Validated academic level creation data
        Returns:
            AcademicLevelResponse: Created academic level
        """
        level = self.factory.create_academic_level(data)
        return AcademicLevelResponse.model_validate(level)


    def get_level(self, level_id: UUID) -> AcademicLevelResponse:
        """Get academic level by ID.
        Args:
            level_id: academic level UUID
        Returns:
            AcademicLevelResponse: Retrieved academic level
        """
        level = self.factory.get_academic_level(level_id)
        return AcademicLevelResponse.model_validate(level)


    def get_all_levels(self, filters: AcademicLevelFilterParams) -> List[AcademicLevelResponse]:
        """Get all active academic level.
        Returns:
            List[QualificationResponse]: List of active academic levels
        """
        levels = self.factory.get_all_academic_levels(filters)
        return [AcademicLevelResponse.model_validate(level) for level in levels]


    def update_level(self, level_id: UUID, data: AcademicLevelUpdate) -> AcademicLevelResponse:
        """Update academic level information.
        Args:
            level_id: academic level UUID
            data: Validated update data
        Returns:
            AcademicLevelResponse: Updated academic level
        """
        data = data.model_dump()
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


    def delete_level(self, level_id: UUID) -> None:
        """Permanently delete a academic level.
        Args:
            level_id: academic level UUID
        """
        self.factory.delete_academic_level(level_id)


    # Archived AcademicLevel operations
    def get_archived_level(self, level_id: UUID) -> AcademicLevelResponse:
        """Get an archived academic level by ID.
        Args:
            level_id: academic level UUID
        Returns:
            AcademicLevelResponse: Retrieved archived academic level
        """
        level = self.factory.get_archived_academic_level(level_id)
        return AcademicLevelResponse.model_validate(level)

    def get_all_archived_levels(self, filters: AcademicLevelFilterParams) -> List[AcademicLevelResponse]:
        """Get all archived academic levels.
        Args:
            filters: Filter parameters
        Returns:
            List[AcademicLevelResponse]: List of archived academic levels
        """
        levels = self.factory.get_all_archived_academic_levels(filters)
        return [AcademicLevelResponse.model_validate(level) for level in levels]


    def restore_level(self, level_id: UUID) -> AcademicLevelResponse:
        """Restore an archived academic level.
        Args:
            level_id: academic level UUID
        Returns:
            AcademicLevelResponse: Restored academic level
        """
        level = self.factory.restore_academic_level(level_id)
        return AcademicLevelResponse.model_validate(level)


    def delete_archived_level(self, level_id: UUID) -> None:
        """Permanently delete an archived academic level.
        Args:
            level_id: academic level UUID
        """
        self.factory.delete_archived_academic_level(level_id)