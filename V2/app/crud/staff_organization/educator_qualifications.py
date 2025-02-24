from ...database.models.data_enums import ArchiveReason
from ...schemas.staff_organization.educator_qualifications import (
    QualificationCreate, QualificationUpdate, QualificationResponse
)
from ...services.staff_organization.factories.educator_qualifications import QualificationsFactory
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List


class QualificationsCrud:
    """CRUD operations for educator qualifications."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        self.factory = QualificationsFactory(session)


    def create_qualification(self, data: QualificationCreate) -> QualificationResponse:
        """Create a new qualification.
        Args:
            data: Validated qualification creation data
        Returns:
            QualificationResponse: Created qualification
        """
        qualification = self.factory.create_qualification(data)
        return QualificationResponse.model_validate(qualification)

    def get_qualification(self, qualification_id: UUID) -> QualificationResponse:
        """Get a qualification by ID.
        Args:
            qualification_id: Qualification UUID
        Returns:
            QualificationResponse: Retrieved qualification
        """
        qualification = self.factory.get_qualification(qualification_id)
        return QualificationResponse.model_validate(qualification)


    def get_all_qualifications(self) -> List[QualificationResponse]:
        """Get all active educator qualifications.
        Returns:
            List[QualificationResponse]: List of active qualifications
        """
        qualifications = self.factory.get_all_qualifications()
        return [QualificationResponse.model_validate(qualification) for qualification in qualifications]


    def update_qualification(self, qualification_id: UUID, data: QualificationUpdate) -> QualificationResponse:
        """Update a qualification.
        Args:
            qualification_id: Qualification UUID
            data: Validated update data
        Returns:
            QualificationResponse: Updated qualification
        """
        data = data.model_dump()
        updated_qualification = self.factory.update_qualification(qualification_id, data)
        return QualificationResponse.model_validate(updated_qualification)

    def archive_qualification(self, qualification_id: UUID, reason: ArchiveReason) -> QualificationResponse:
        """Archive a qualification.
        Args:
            qualification_id: Qualification UUID
            reason: Reason for archiving
        Returns:
            QualificationResponse: Archived qualification
        """
        qualification = self.factory.archive_qualification(qualification_id, reason)
        return QualificationResponse.model_validate(qualification)


    def delete_qualification(self, qualification_id: UUID) -> None:
        """Permanently delete a qualification.
        Args:
            qualification_id: Qualification UUID
        """
        self.factory.delete_qualification(qualification_id)