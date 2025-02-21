from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .validators import staff_organisation_validators
from ..base_crud import CrudService
from ...database.models.staff_organization import EducatorQualifications
from ...database.models.data_enums import ArchiveReason
from V2.app.services.errors.staff_organisation_errors import QualificationNotFoundError, DuplicateQualificationError
from ...schemas.staff_organization.educator_qualifications import (
    QualificationCreate,
    QualificationResponse,
    QualificationUpdate
)

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class EducatorQualificationsService(CrudService):
    """Service class for managing educator qualification operations."""

    def __init__(self, db: Session):
        super().__init__(db, EducatorQualifications)
        self.validator = staff_organisation_validators

    def create_qualification(self, new_qualification: QualificationCreate) -> QualificationResponse:
        """Create a new educator qualification."""
        qualification = EducatorQualifications(
            id=uuid4(),
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
            educator_id=new_qualification.educator_id,
            name=self.validator.validate_name(new_qualification.name),
            description=self.validator.validate_name(new_qualification.description)
        )

        try:
            self.db.add(qualification)
            self.db.commit()
            return QualificationResponse.model_validate(qualification)
        except IntegrityError:
            self.db.rollback()
            raise DuplicateQualificationError(qualification.name)

    def get_qualifications(self) -> list[QualificationResponse]:
        """Get all active educator qualifications."""
        qualifications = (self.base_query()
                          .order_by(EducatorQualifications.name).all())
        return [QualificationResponse.model_validate(qualification)
                for qualification in qualifications]

    def get_qualification(self, qualification_id: UUID) -> QualificationResponse:
        """Get a specific qualification by ID."""
        qualification = (self.base_query()
                         .filter(EducatorQualifications.id == qualification_id)
                         .first())
        if not qualification:
            raise QualificationNotFoundError
        return QualificationResponse.model_validate(qualification)

    def update_qualification(self, qualification_id: UUID,
                             data: QualificationUpdate) -> QualificationResponse:
        """Update a qualification's information."""
        data_update = data.model_dump(exclude_unset=True)
        if 'name' in data_update:
            data.name = self.validator.validate_name(data.name)
        if 'description' in data_update:
            data.description = self.validator.validate_name(data.description)

        qualification = self.get_qualification(qualification_id)
        try:
            for key, value in data_update.items():
                setattr(qualification, key, value)
            qualification.last_modified_by = SYSTEM_USER_ID #placeholder

            self.db.commit()
            self.db.refresh(qualification)
            return QualificationResponse.model_validate(qualification)
        except IntegrityError:
            self.db.rollback()
            raise DuplicateQualificationError(data.get('name'))

    def archive_qualification(self, qualification_id: UUID,
                              reason: ArchiveReason) -> QualificationResponse:
        """Archive an educator qualification."""
        qualification = self.get_qualification(qualification_id)
        qualification.archive(SYSTEM_USER_ID, reason)

        self.db.commit()
        self.db.refresh(qualification)
        return QualificationResponse.model_validate(qualification)

    def delete_qualification(self, qualification_id: UUID) -> None:
        """Permanently delete an educator qualification."""
        qualification = self.get_qualification(qualification_id)
        self.db.delete(qualification)
        self.db.commit()