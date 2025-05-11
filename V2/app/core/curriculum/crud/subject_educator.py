from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.curriculum.factories.subject_educator import SubjectEducatorFactory
from V2.app.core.curriculum.models.curriculum import SubjectEducator
from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.curriculum.schemas.subject_educator import (
    SubjectEducatorFilterParams, SubjectEducatorCreate, SubjectEducatorResponse

)

class SubjectEducatorCrud:
    """CRUD operations for academic subject educators."""

    def __init__(self, session: Session, current_user = None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.current_user = current_user
        self.factory = SubjectEducatorFactory(session, current_user=current_user)
        self.export_service = ExportService(session)


    def create_subject_educator(self, educator_id: UUID, data: SubjectEducatorCreate) -> SubjectEducatorResponse:
        """Assign a new subject to an educator."""
        new_subject = self.factory.create_subject_educator(educator_id, data)
        return SubjectEducatorResponse.model_validate(new_subject)


    def get_subject_educator(self, subject_educator_id: UUID) -> SubjectEducatorResponse:
        """Get a subject educator by ID."""
        subject_response = self.factory.get_subject_educator(subject_educator_id)
        return SubjectEducatorResponse.model_validate(subject_response)


    def get_all_subject_educators(self, filters: SubjectEducatorFilterParams) -> List[SubjectEducatorResponse]:
        """Get all active educators assignments for all subjects."""
        subject_educators = self.factory.get_all_subject_educators(filters)
        return [SubjectEducatorResponse.model_validate(subject) for subject in subject_educators]


    def archive_subject_educator(self, subject_educator_id: UUID, reason: ArchiveReason) -> None:
        """Archive a subject assignment.
        Args:
            subject_educator_id: subject educator UUID
            reason: Reason for archiving
        Returns:
            SubjectEducatorResponse: Archived subject assignment
        """
        self.factory.archive_subject_educator(subject_educator_id, reason)


    def export_subject_educator(self, subject_educator_id: UUID, export_format: str) -> str:
        """Export subject educator and its associated data
        Args:
            subject_educator_id: subject educator UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            SubjectEducator, subject_educator_id, export_format
        )


    def delete_subject_educator(self, subject_educator_id: UUID) -> None:
        """Permanently delete a subject educator"""
        self.factory.delete_subject_educator(subject_educator_id)


    # Archived operations
    def get_archived_subject_educator(self, subject_educator_id: UUID) -> SubjectEducatorResponse:
        """Get an archived subject assignment by ID."""
        subject_response = self.factory.get_archived_subject_educator(subject_educator_id)
        return SubjectEducatorResponse.model_validate(subject_response)


    def get_all_archived_subject_educators(self, filters: SubjectEducatorFilterParams) -> List[SubjectEducatorResponse]:
        """Get all archived subject assignment."""
        subjects = self.factory.get_all_archived_subject_educators(filters)
        return [SubjectEducatorResponse.model_validate(subject) for subject in subjects]


    def restore_subject_educator(self, subject_educator_id: UUID) -> SubjectEducatorResponse:
        """Restore an archived subject assignment."""
        restored_subject = self.factory.restore_subject_educator(subject_educator_id)
        return SubjectEducatorResponse.model_validate(restored_subject)


    def delete_archived_subject_educator(self, subject_educator_id: UUID) -> None:
        """Permanently delete an archived subject assignment."""
        self.factory.delete_archived_subject_educator(subject_educator_id)