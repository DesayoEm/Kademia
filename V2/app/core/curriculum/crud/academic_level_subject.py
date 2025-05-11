from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from V2.app.core.curriculum.factories.academic_level_subject import AcademicLevelSubjectFactory
from V2.app.core.curriculum.models.curriculum import AcademicLevelSubject
from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.curriculum.schemas.academic_level_subject import (
    AcademicLevelSubjectFilterParams, AcademicLevelSubjectCreate, AcademicLevelSubjectResponse
)


class AcademicLevelSubjectCrud:
    """CRUD operations for academic level subjects."""

    def __init__(self, session: Session, current_user = None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.current_user = current_user
        self.factory = AcademicLevelSubjectFactory(session, current_user=current_user)
        self.export_service = ExportService(session)


    def create_level_subject(self, level_id: UUID, data: AcademicLevelSubjectCreate) -> AcademicLevelSubjectResponse:
        """Assign a new subject to an academic level."""
        new_subject = self.factory.create_academic_level_subject(level_id, data)
        return AcademicLevelSubjectResponse.model_validate(new_subject)


    def get_level_subject(self, level_subject_id: UUID) -> AcademicLevelSubjectResponse:
        """Get academic level subject by ID."""
        subject_response = self.factory.get_academic_level_subject(level_subject_id)
        return AcademicLevelSubjectResponse.model_validate(subject_response)


    def get_all_level_subjects(self, filters: AcademicLevelSubjectFilterParams) -> List[AcademicLevelSubjectResponse]:
        """Get all active subjects for all academic levels."""
        level_subjects = self.factory.get_all_academic_level_subjects(filters)
        return [AcademicLevelSubjectResponse.model_validate(subject) for subject in level_subjects]


    def archive_level_subject(self, level_subject_id: UUID, reason: ArchiveReason) -> None:
        """Archive a subject."""
        self.factory.archive_academic_level_subject(level_subject_id, reason)

    def export_level_subject(self, level_subject_id: UUID, export_format: str) -> str:
        """Export level subject and its associated data
        Args:
            level_subject_id: level subject UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            AcademicLevelSubject, level_subject_id, export_format
        )


    def delete_level_subject(self, level_subject_id: UUID) -> None:
        """Permanently delete a level subject.
        Args:
            level_subject_id: level subject UUID
        """
        self.factory.delete_academic_level_subject(level_subject_id)


    # Archived subject operations
    def get_archived_level_subject(self, level_subject_id: UUID) -> AcademicLevelSubjectResponse:
        """Get an archived subject by ID."""
        subject_response = self.factory.get_archived_academic_level_subject(level_subject_id)
        return AcademicLevelSubjectResponse.model_validate(subject_response)


    def get_all_archived_level_subjects(self, filters: AcademicLevelSubjectFilterParams) -> List[AcademicLevelSubjectResponse]:
        """Get all archived student_organization."""
        subjects = self.factory.get_all_archived_academic_level_subjects(filters)
        return [AcademicLevelSubjectResponse.model_validate(subject) for subject in subjects]


    def restore_level_subject(self, level_subject_id: UUID) -> AcademicLevelSubjectResponse:
        """Restore an archived subject."""
        restored_subject = self.factory.restore_academic_level_subject(level_subject_id)
        return AcademicLevelSubjectResponse.model_validate(restored_subject)


    def delete_archived_level_subject(self, level_subject_id: UUID) -> None:
        """Permanently delete an archived subject."""
        self.factory.delete_archived_academic_level_subject(level_subject_id)