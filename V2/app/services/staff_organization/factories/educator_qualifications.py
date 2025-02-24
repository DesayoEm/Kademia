from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from V2.app.services.staff_organization.validators import StaffOrganizationValidators
from V2.app.database.models.staff_organization import EducatorQualifications
from V2.app.database.db_repositories.sqlalchemy_repos.core_repo import SQLAlchemyRepository
from V2.app.database.models.data_enums import ArchiveReason


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class QualificationsFactory:
    """Factory class for managing qualification operations."""

    def __init__(self, session: Session):
        """Initialize factory with database session.
        Args:
            session: SQLAlchemy database session
        """
        self.repository = SQLAlchemyRepository(EducatorQualifications, session)
        self.validator = StaffOrganizationValidators()

    def create_qualification(self, new_qualification) -> EducatorQualifications:
        """Create a new qualification.
        Args:
            new_qualification: Qualification data containing name, description and owner
        Returns:
            EducatorQualifications: Created qualification record
        """
        qualification = EducatorQualifications(
            id=uuid4(),
            educator_id = SYSTEM_USER_ID,
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
            name=self.validator.validate_name(new_qualification.name),
            description=self.validator.validate_name(new_qualification.description)
        )
        return self.repository.create(qualification)


    def get_all_qualifications(self) -> List[EducatorQualifications]:
        """Get all active qualifications.
        Returns:
            List[EducatorQualifications]: List of active qualification records
        """
        return self.repository.get_all()


    def get_qualification(self, qualification_id: UUID) -> EducatorQualifications:
        """Get a specific qualification by ID.
        Args:
            qualification_id: ID of qualification to retrieve
        Returns:
            EducatorQualifications: Retrieved qualification record
        """
        return self.repository.get_by_id(qualification_id)


    def update_qualification(self, qualification_id: UUID, data: dict) -> EducatorQualifications:
        """Update a qualification's information.
        Args:
            qualification_id: ID of qualification to update
            data: Dictionary containing fields to update
        Returns:
            EducatorQualifications: Updated qualification record
        """

        existing = self.get_qualification(qualification_id)
        if 'name' in data:
            existing.name = self.validator.validate_name(data['name'])
        if 'description' in data:
            existing.description = self.validator.validate_name(data['description'])
        existing.last_modified_by = SYSTEM_USER_ID

        return self.repository.update(qualification_id, existing)


    def archive_qualification(self, qualification_id: UUID, reason: ArchiveReason) -> EducatorQualifications:
        """Archive a qualification.
        Args:
            qualification_id: ID of qualification to archive
            reason: Reason for archiving
        Returns:
            EducatorQualifications: Archived qualification record
        """
        return self.repository.archive(qualification_id, SYSTEM_USER_ID, reason)


    def delete_qualification(self, qualification_id: UUID) -> None:
        """Permanently delete a qualification.
        Args:
            qualification_id: ID of qualification to delete
        """
        self.repository.delete(qualification_id)



