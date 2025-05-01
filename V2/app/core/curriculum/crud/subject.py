from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.curriculum.models.curriculum import Subject
from V2.app.core.curriculum.factories.subject import SubjectFactory
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.curriculum.schemas.subject import (
    SubjectCreate, SubjectUpdate, SubjectResponse, SubjectFilterParams
)


class SubjectCrud:
    """CRUD operations for subjects."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
        """
        self.session = session
        self.factory = SubjectFactory(session)
        self.export_service = ExportService(session)


    def create_subject(self, data: SubjectCreate) -> SubjectResponse:
        """Create a new subject.
        Args:
            data: Validated subject creation data
        Returns:
            SubjectResponse: Created subject
        """
        new_subject = self.factory.create_subject(data)
        return SubjectResponse.model_validate(new_subject)


    def get_subject(self, subject_id: UUID) -> SubjectResponse:
        """Get subject by ID.
        Args:
            subject_id: subject UUID
        Returns:
            SubjectResponse: Retrieved subject
        """
        subject_response = self.factory.get_subject(subject_id)
        return SubjectResponse.model_validate(subject_response)


    def get_all_subjects(self, filters: SubjectFilterParams) -> List[SubjectResponse]:
        """Get all active subjects.
        Returns:
            List[SubjectResponse]: List of active student_organization
        """
        subjects = self.factory.get_all_subjects(filters)
        return [SubjectResponse.model_validate(subject) for subject in subjects]


    def update_subject(self, subject_id: UUID, data: SubjectUpdate) -> SubjectResponse:
        """Update subject information.
        Args:
            subject_id: subject UUID
            data: Validated update data
        Returns:
            SubjectResponse: Updated subject
        """
        data = data.model_dump(exclude_unset=True)
        updated_subject = self.factory.update_subject(subject_id, data)
        return SubjectResponse.model_validate(updated_subject)


    def archive_subject(self, subject_id: UUID, reason: ArchiveReason) -> None:
        """Archive a subject.
        Args:
            subject_id: subject UUID
            reason: Reason for archiving
        Returns:
            SubjectResponse: Archived subject
        """
        self.factory.archive_subject(subject_id, reason)

    def export_subject(self, subject_id: UUID, export_format: str) -> str:
        """Export subject and its associated data
        Args:
            subject_id: subject UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Subject, subject_id, export_format
        )


    def delete_subject(self, subject_id: UUID) -> None:
        """Permanently delete a subject.
        Args:
            subject_id: subject UUID
        """
        self.factory.delete_subject(subject_id)


    # Archived subject operations
    def get_archived_subject(self, subject_id: UUID) -> SubjectResponse:
        """Get an archived subject by ID.
        Args:
            subject_id: subject UUID
        Returns:
            SubjectResponse: Retrieved archived subject
        """
        subject_response = self.factory.get_archived_subject(subject_id)
        return SubjectResponse.model_validate(subject_response)

    def get_all_archived_subjects(self, filters: SubjectFilterParams) -> List[SubjectResponse]:
        """Get all archived student_organization.
        Args:
            filters: Filter parameters
        Returns:
            List[SubjectResponse]: List of archived student_organization
        """
        subjects = self.factory.get_all_archived_subjects(filters)
        return [SubjectResponse.model_validate(subject) for subject in subjects]


    def restore_subject(self, subject_id: UUID) -> SubjectResponse:
        """Restore an archived subject.
        Args:
            subject_id: subject UUID
        Returns:
            SubjectResponse: Restored subject
        """
        restored_subject = self.factory.restore_subject(subject_id)
        return SubjectResponse.model_validate(restored_subject)


    def delete_archived_subject(self, subject_id: UUID) -> None:
        """Permanently delete an archived subject.
        Args:
            subject_id: subject UUID
        """
        self.factory.delete_archived_subject(subject_id)