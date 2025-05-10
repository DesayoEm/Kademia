from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.staff_management.models.staff_management import EducatorQualification
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.staff_management.factories.qualification import QualificationFactory
from V2.app.core.staff_management.schemas.qualification import (
    QualificationCreate, QualificationUpdate, QualificationResponse, QualificationFilterParams
)


class QualificationCrud:
    """CRUD operations for educator qualifications."""

    def __init__(self, session: Session, current_user = None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
        """
        self.session = session
        self.current_user = current_user
        self.factory = QualificationFactory(session, current_user = current_user)
        self.export_service = ExportService(session)


    # Active qualification operations
    def create_qualification(self, educator_id: UUID, data: QualificationCreate) -> QualificationResponse:
        """Create a new qualification."""
        qualification = self.factory.create_qualification(educator_id, data)
        return QualificationResponse.model_validate(qualification)


    def get_qualification(self,qualification_id: UUID) -> QualificationResponse:
        """Get a qualification by ID."""
        qualification = self.factory.get_qualification(qualification_id)
        return QualificationResponse.model_validate(qualification)


    def get_all_qualifications(self, filters: QualificationFilterParams) -> List[QualificationResponse]:
        """Get all active educator qualifications."""
        qualifications = self.factory.get_all_qualifications(filters)
        return [QualificationResponse.model_validate(qualification) for qualification in qualifications]


    def update_qualification(self, qualification_id: UUID, data: QualificationUpdate) -> QualificationResponse:
        """Update a qualification."""
        data = data.model_dump(exclude_unset=True)
        updated_qualification = self.factory.update_qualification(qualification_id, data)
        return QualificationResponse.model_validate(updated_qualification)


    def archive_qualification(self, qualification_id: UUID, reason: ArchiveReason) -> None:
        """Archive a qualification.
        Args:
            qualification_id: Qualification UUID
            reason: Reason for archiving
        Returns:
            QualificationResponse: Archived qualification
        """
        self.factory.archive_qualification(qualification_id, reason)


    def export_qualification(self, qualification_id: UUID, export_format: str) -> str:
        """Export qualification and its associated data
        Args:
            qualification_id: Qualification UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            EducatorQualification, qualification_id, export_format
        )


    def delete_qualification(self, qualification_id: UUID) -> None:
        """Permanently delete a qualification."""
        self.factory.delete_qualification(qualification_id)


    # Archived qualification operations
    def get_archived_qualification(self, qualification_id: UUID) -> QualificationResponse:
        """Get an archived qualification by ID."""
        qualification = self.factory.get_archived_qualification(qualification_id)
        return QualificationResponse.model_validate(qualification)


    def get_all_archived_qualifications(self, filters: QualificationFilterParams) -> List[QualificationResponse]:
        """Get all archived educator qualifications."""
        qualifications = self.factory.get_all_archived_qualifications(filters)
        return [QualificationResponse.model_validate(qualification) for qualification in qualifications]


    def restore_qualification(self, qualification_id: UUID) -> QualificationResponse:
        """Restore an archived qualification."""
        qualification = self.factory.restore_qualification(qualification_id)
        return QualificationResponse.model_validate(qualification)


    def delete_archived_qualification(self, qualification_id: UUID) -> None:
        """Permanently delete an archived qualification."""
        self.factory.delete_archived_qualification(qualification_id)