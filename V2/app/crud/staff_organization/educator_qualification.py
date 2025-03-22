from ...database.models.data_enums import ArchiveReason
from ...schemas.staff_organization.educator_qualification import (
    QualificationCreate, QualificationUpdate, QualificationResponse, QualificationFilterParams
)
from ...core.factories.staff_organization.qualification import QualificationFactory
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List


class QualificationCrud:
    """CRUD operations for educator qualifications."""

    def __init__(self, session: Session):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy database session
        """
        self.session = session
        self.factory = QualificationFactory(session)

    # Active qualification operations
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


    def get_all_qualifications(self, filters: QualificationFilterParams) -> List[QualificationResponse]:
        """Get all active educator qualifications.
        Args:
            filters: Filter parameters
        Returns:
            List[QualificationResponse]: List of active qualifications
        """
        qualifications = self.factory.get_all_qualifications(filters)
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

    def archive_qualification(self, qualification_id: UUID, reason: ArchiveReason) -> None:
        """Archive a qualification.
        Args:
            qualification_id: Qualification UUID
            reason: Reason for archiving
        Returns:
            QualificationResponse: Archived qualification
        """
        self.factory.archive_qualification(qualification_id, reason)


    def delete_qualification(self, qualification_id: UUID) -> None:
        """Permanently delete a qualification.
        Args:
            qualification_id: Qualification UUID
        """
        self.factory.delete_qualification(qualification_id)

    # Archived qualification operations
    def get_archived_qualification(self, qualification_id: UUID) -> QualificationResponse:
        """Get an archived qualification by ID.
        Args:
            qualification_id: Qualification UUID
        Returns:
            QualificationResponse: Retrieved archived qualification
        """
        qualification = self.factory.get_archived_qualification(qualification_id)
        return QualificationResponse.model_validate(qualification)

    def get_all_archived_qualifications(self, filters: QualificationFilterParams) -> List[QualificationResponse]:
        """Get all archived educator qualifications.
        Args:
            filters: Filter parameters
        Returns:
            List[QualificationResponse]: List of archived qualifications
        """
        qualifications = self.factory.get_all_archived_qualifications(filters)
        return [QualificationResponse.model_validate(qualification) for qualification in qualifications]

    def restore_qualification(self, qualification_id: UUID) -> QualificationResponse:
        """Restore an archived qualification.
        Args:
            qualification_id: Qualification UUID
        Returns:
            QualificationResponse: Restored qualification
        """
        qualification = self.factory.restore_qualification(qualification_id)
        return QualificationResponse.model_validate(qualification)


    def delete_archived_qualification(self, qualification_id: UUID) -> None:
        """Permanently delete an archived qualification.
        Args:
            qualification_id: Qualification UUID
        """
        self.factory.delete_archived_qualification(qualification_id)