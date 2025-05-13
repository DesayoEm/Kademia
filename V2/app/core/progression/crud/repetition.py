from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.progression.models.progression import Repetition
from V2.app.core.progression.schemas.repetition import (
    StudentRepetitionCreate,
    StudentRepetitionResponse,
    RepetitionFilterParams
)
from V2.app.core.progression.factories.repetition import RepetitionFactory
from V2.app.core.shared.schemas.enums import ArchiveReason


class RepetitionCrud:
    """CRUD operations for student repetitions."""

    def __init__(self, session: Session, current_user = None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.current_user = current_user
        self.factory = RepetitionFactory(session, current_user=current_user)


    def create_repetition(self, student_id: UUID, data: StudentRepetitionCreate) -> StudentRepetitionResponse:
        """Create a new repetition record for a student."""
        repetition = self.factory.create_repetition(student_id, data)
        return StudentRepetitionResponse.model_validate(repetition)


    def get_repetition(self, repetition_id: UUID) -> StudentRepetitionResponse:
        """Get a specific repetition record by ID."""
        repetition = self.factory.get_repetition(repetition_id)
        return StudentRepetitionResponse.model_validate(repetition)


    def get_all_repetitions(self, filters: RepetitionFilterParams) -> List[StudentRepetitionResponse]:
        """Get all active repetition records."""
        repetitions = self.factory.get_all_repetitions(filters)
        return [StudentRepetitionResponse.model_validate(rep) for rep in repetitions]


    def update_repetition(self, repetition_id: UUID, data: dict) -> StudentRepetitionResponse:
        """Update an existing repetition record."""
        updated = self.factory.update_repetition(repetition_id, data.model_dump(exclude_unset=True))
        return StudentRepetitionResponse.model_validate(updated)

    def archive_repetition(self, repetition_id: UUID, reason: ArchiveReason) -> None:
        """Archive a repetition record."""
        self.factory.archive_repetition(repetition_id, reason)

    def delete_repetition(self, repetition_id: UUID) -> None:
        """Permanently delete a repetition record."""
        self.factory.delete_repetition(repetition_id)

    def get_archived_repetition(self, repetition_id: UUID) -> StudentRepetitionResponse:
        """Get an archived repetition record by ID."""
        archived = self.factory.get_archived_repetition(repetition_id)
        return StudentRepetitionResponse.model_validate(archived)

    def get_all_archived_repetitions(self, filters: RepetitionFilterParams) -> List[StudentRepetitionResponse]:
        """Get all archived repetition records."""
        repetitions = self.factory.get_all_archived_repetitions(filters)
        return [StudentRepetitionResponse.model_validate(rep) for rep in repetitions]

    def restore_repetition(self, repetition_id: UUID) -> StudentRepetitionResponse:
        """Restore an archived repetition record."""
        restored = self.factory.restore_repetition(repetition_id)
        return StudentRepetitionResponse.model_validate(restored)

    def delete_archived_repetition(self, repetition_id: UUID) -> None:
        """Permanently delete an archived repetition record."""
        self.factory.delete_archived_repetition(repetition_id)
