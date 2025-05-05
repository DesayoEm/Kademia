from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.progression.models.progression import Graduation
from V2.app.core.progression.schemas.graduation import (
    GraduationCreate,
    GraduationResponse,
    GraduationFilterParams
)
from V2.app.core.progression.factories.graduation import GraduationFactory
from V2.app.core.shared.schemas.enums import ArchiveReason


class GraduationCrud:
    """CRUD operations for student graduations."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
        """
        self.session = session
        self.factory = GraduationFactory(session)

    def create_graduation(self, student_id: UUID, data: GraduationCreate) -> GraduationResponse:
        """Create a new graduation record for a student."""
        graduation = self.factory.create_graduation(student_id, data)
        return GraduationResponse.model_validate(graduation)

    def get_graduation(self, graduation_id: UUID) -> GraduationResponse:
        """Get a specific graduation record by ID."""
        graduation = self.factory.get_graduation(graduation_id)
        return GraduationResponse.model_validate(graduation)

    def get_all_graduations(self, filters: GraduationFilterParams) -> List[GraduationResponse]:
        """Get all active graduation records."""
        graduations = self.factory.get_all_graduations(filters)
        return [GraduationResponse.model_validate(g) for g in graduations]

    def update_graduation(self, graduation_id: UUID, data: dict) -> GraduationResponse:
        """Update an existing graduation record."""
        updated = self.factory.update_graduation(graduation_id, data.model_dump(exclude_unset=True))
        return GraduationResponse.model_validate(updated)

    def archive_graduation(self, graduation_id: UUID, reason: ArchiveReason) -> None:
        """Archive a graduation record."""
        self.factory.archive_graduation(graduation_id, reason)

    def delete_graduation(self, graduation_id: UUID) -> None:
        """Permanently delete a graduation record."""
        self.factory.delete_graduation(graduation_id)

    def get_archived_graduation(self, graduation_id: UUID) -> GraduationResponse:
        """Get an archived graduation record by ID."""
        archived = self.factory.get_archived_graduation(graduation_id)
        return GraduationResponse.model_validate(archived)

    def get_all_archived_graduations(self, filters: GraduationFilterParams) -> List[GraduationResponse]:
        """Get all archived graduation records."""
        graduations = self.factory.get_all_archived_graduations(filters)
        return [GraduationResponse.model_validate(g) for g in graduations]

    def restore_graduation(self, graduation_id: UUID) -> GraduationResponse:
        """Restore an archived graduation record."""
        restored = self.factory.restore_graduation(graduation_id)
        return GraduationResponse.model_validate(restored)

    def delete_archived_graduation(self, graduation_id: UUID) -> None:
        """Permanently delete an archived graduation record."""
        self.factory.delete_archived_graduation(graduation_id)
