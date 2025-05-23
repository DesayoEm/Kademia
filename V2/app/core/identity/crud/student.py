from uuid import UUID
from typing import List
from sqlalchemy.orm import Session

from V2.app.core.identity.models.student import Student
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.identity.factories.student import StudentFactory
from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.identity.schemas.student import (
    StudentCreate, StudentUpdate, StudentResponse, StudentFilterParams
)

class StudentCrud:
    """CRUD operations for students."""

    def __init__(self, session: Session, current_user=None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.current_user = current_user
        self.factory = StudentFactory(session, current_user=current_user)
        self.export_service = ExportService(session)


    def create_student(self, data: StudentCreate) -> StudentResponse:
        """Create a new student."""
        student = self.factory.create_student(data)
        return StudentResponse.model_validate(student)


    def get_student(self, student_id: UUID) -> StudentResponse:
        """Get student by ID."""
        student = self.factory.get_student(student_id)
        return StudentResponse.model_validate(student)


    def get_all_students(self, filters: StudentFilterParams) -> List[StudentResponse]:
        """Get all active student."""
        students = self.factory.get_all_students(filters)
        return [StudentResponse.model_validate(student) for student in students]


    def update_student(self, student_id: UUID, data: StudentUpdate) -> StudentResponse:
        """Update student information."""
        data = data.model_dump()
        updated_student = self.factory.update_student(student_id, data)
        return StudentResponse.model_validate(updated_student)


    def archive_student(self, student_id: UUID, reason: ArchiveReason) -> None:
        """Archive a student.
        Args:
            student_id: student UUID
            reason: Reason for archiving
        Returns:
            StudentResponse: Archived student
        """
        self.factory.archive_student(student_id, reason)


    def export_student(self, student_id: UUID, export_format: str) -> str:
        """Export guardian and its associated data
        Args:
            student_id: student UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            Student, student_id, export_format
        )


    def delete_student(self, student_id: UUID) -> None:
        """Permanently delete a student."""
        self.factory.delete_student(student_id)


    # Archived student operations
    def get_archived_student(self, student_id: UUID) -> StudentResponse:
        """Get an archived student by ID."""
        student = self.factory.get_archived_student(student_id)
        return StudentResponse.model_validate(student)


    def get_all_archived_student(self, filters: StudentFilterParams) -> List[StudentResponse]:
        """Get all archived student."""
        all_student = self.factory.get_all_archived_students(filters)
        return [StudentResponse.model_validate(student) for student in all_student]


    def restore_student(self, student_id: UUID) -> StudentResponse:
        """Restore an archived student."""
        student = self.factory.restore_student(student_id)
        return StudentResponse.model_validate(student)


    def delete_archived_student(self, student_id: UUID) -> None:
        """Permanently delete an archived student."""
        self.factory.delete_archived_student(student_id)