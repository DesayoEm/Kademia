from sqlalchemy.orm import Session
from uuid import UUID

from typing import List
from V2.app.core.curriculum.factories.student_subject import StudentSubjectFactory
from V2.app.core.curriculum.models.curriculum import StudentSubject
from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.curriculum.schemas.student_subject import (
    StudentSubjectFilterParams, StudentSubjectCreate, StudentSubjectResponse

)


class StudentSubjectCrud:
    """CRUD operations for academic student subjects."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
        """
        self.session = session
        self.factory = StudentSubjectFactory(session)
        self.export_service = ExportService(session)


    def create_student_subject(self, data: StudentSubjectCreate) -> StudentSubjectResponse:
        """Assign a new subject to a student.
        Args:
            data: Validated subject creation data
        Returns:
            StudentSubjectResponse: Created subject
        """
        new_subject = self.factory.create_student_subject(data)
        return StudentSubjectResponse.model_validate(new_subject)


    def get_student_subject(self, student_subject_id: UUID) -> StudentSubjectResponse:
        """Get academic student subject by ID.
        Args:
            student_subject_id: student subject UUID
        Returns:
            StudentSubjectResponse: Retrieved subject
        """
        subject_response = self.factory.get_student_subject(student_subject_id)
        return StudentSubjectResponse.model_validate(subject_response)


    def get_all_student_subjects(self, filters: StudentSubjectFilterParams) -> List[StudentSubjectResponse]:
        """Get all active subjects for all students.
        Returns:
            List[StudentSubjectResponse]: List of active student_organization
        """
        student_subjects = self.factory.get_all_student_subjects(filters)
        return [StudentSubjectResponse.model_validate(subject) for subject in student_subjects]


    def archive_student_subject(self, student_subject_id: UUID, reason: ArchiveReason) -> None:
        """Archive a subject.
        Args:
            student_subject_id: student subject UUID
            reason: Reason for archiving
        Returns:
            StudentSubjectResponse: Archived subject
        """
        self.factory.archive_student_subject(student_subject_id, reason)

    def export_student_subject(self, student_subject_id: UUID, export_format: str) -> str:
        """Export student subject and its associated data
        Args:
            student_subject_id: student subject UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            StudentSubject, student_subject_id, export_format
        )


    def delete_student_subject(self, student_subject_id: UUID) -> None:
        """Permanently delete a student subject.
        Args:
            student_subject_id: student subject UUID
        """
        self.factory.delete_student_subject(student_subject_id)


    # Archived subject operations
    def get_archived_student_subject(self, student_subject_id: UUID) -> StudentSubjectResponse:
        """Get an archived subject by ID.
        Args:
            student_subject_id: student subject UUID
        Returns:
            StudentSubjectResponse: Retrieved archived subject
        """
        subject_response = self.factory.get_archived_student_subject(student_subject_id)
        return StudentSubjectResponse.model_validate(subject_response)

    def get_all_archived_student_subjects(self, filters: StudentSubjectFilterParams) -> List[StudentSubjectResponse]:
        """Get all archived subject assignment.
        Args:
            filters: Filter parameters
        Returns:
            List[StudentSubjectResponse]: List of archived student subjects
        """
        subjects = self.factory.get_all_archived_student_subjects(filters)
        return [StudentSubjectResponse.model_validate(subject) for subject in subjects]


    def restore_student_subject(self, student_subject_id: UUID) -> StudentSubjectResponse:
        """Restore an archived subject assignment.
        Args:
            student_subject_id: student subject UUID
        Returns:
            StudentSubjectResponse: Restored subject assignment
        """
        restored_subject = self.factory.restore_student_subject(student_subject_id)
        return StudentSubjectResponse.model_validate(restored_subject)


    def delete_archived_student_subject(self, student_subject_id: UUID) -> None:
        """Permanently delete an archived subject assignment.
        Args:
            student_subject_id: student subject UUID
        """
        self.factory.delete_archived_student_subject(student_subject_id)