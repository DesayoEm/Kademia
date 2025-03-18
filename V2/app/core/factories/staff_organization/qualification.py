from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from ....core.errors.profile_errors import RelatedEducatorNotFoundError
from ....core.validators.staff_organization import StaffOrganizationValidators
from ....database.models.staff_organization import EducatorQualifications
from ....database.db_repositories.sqlalchemy_repos.main_repo import SQLAlchemyRepository
from ....database.models.data_enums import ArchiveReason
from ....core.errors.database_errors import (
    EntityNotFoundError, UniqueViolationError, RelationshipError)
from ....core.errors.staff_organisation_errors import QualificationNotFoundError, DuplicateQualificationError


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
            name=self.validator.validate_name(new_qualification.name),
            description=self.validator.validate_name(new_qualification.description),
            educator_id=SYSTEM_USER_ID,#Placeholder
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,

        )
        try:
            return self.repository.create(qualification)
        except UniqueViolationError as e:
            raise DuplicateQualificationError(#name is the only field with a unique constraint
                input_value=new_qualification.name, detail=str(e), field = 'name'
            )
        except RelationshipError as e:
            error_message = str(e)
            fk_error_mapping = {
                'educator_id': RelatedEducatorNotFoundError,
            }
            for field, error_class in fk_error_mapping.items():
                if field in error_message:
                    if hasattr(new_qualification, field):
                        entity_id = getattr(new_qualification, field)
                        raise error_class(id=entity_id, detail=str(e), action='create')
                    else:
                        raise RelationshipError(error=str(e), operation='create', entity='unknown')


    def get_all_qualifications(self, filters) -> List[EducatorQualifications]:
        """Get all active qualifications with filtering.
        Returns:
            List[EducatorQualifications]: List of active qualification records
        """
        fields = ['name', 'description']
        return self.repository.execute_query(fields, filters)


    def get_qualification(self, qualification_id: UUID) -> EducatorQualifications:
        """Get a specific qualification by ID.
        Args:
            qualification_id: ID of qualification to retrieve
        Returns:
            EducatorQualifications: Retrieved qualification record
        """
        try:
            return self.repository.get_by_id(qualification_id)
        except EntityNotFoundError as e:
            error_message = str(e)
            raise QualificationNotFoundError(id=qualification_id, detail = error_message)

    def update_qualification(self, qualification_id: UUID, data: dict) -> EducatorQualifications:
        """Update a qualification's information.
        Args:
            qualification_id: ID of qualification to update
            data: Dictionary containing fields to update
        Returns:
            EducatorQualifications: Updated qualification record
        """
        try:
            existing = self.get_qualification(qualification_id)
            educator_id = existing.educator_id  # store separately for error handling

            if 'name' in data:
                existing.name = self.validator.validate_name(data['name'])
            if 'description' in data:
                existing.description = self.validator.validate_name(data['description'])
            existing.last_modified_by = SYSTEM_USER_ID

            return self.repository.update(qualification_id, existing)
        except EntityNotFoundError as e:
            raise QualificationNotFoundError(id=qualification_id, detail=str(e))

        except UniqueViolationError as e:  # name is the only field with a unique constraint
            raise DuplicateQualificationError(
                input_value=data.get('name', ''), detail=str(e), field='name'
            )
        except RelationshipError as e:  # edge case-educator is deleted(race condition)
            error_message = str(e)
            fk_error_mapping = {
                'educator_id': RelatedEducatorNotFoundError,
            }
            for field, error_class in fk_error_mapping.items():
                if field in error_message:
                    if field in data:
                        entity_id = data[field]
                    elif field == 'educator_id' and 'educator_id' in locals():
                        entity_id = educator_id
                    else:
                        raise RelationshipError(error=str(e), operation='update', entity='unknown_entity')
                    raise error_class(id=entity_id, detail=str(e), action='update')


    def archive_qualification(self, qualification_id: UUID, reason: ArchiveReason) -> EducatorQualifications:
        """Archive a qualification.
        Args:
            qualification_id: ID of qualification to archive
            reason: Reason for archiving
        Returns:
            EducatorQualifications: Archived qualification record
        """
        try:
            return self.repository.archive(qualification_id, SYSTEM_USER_ID, reason)
        except EntityNotFoundError as e:
            raise QualificationNotFoundError(id=qualification_id, detail = str(e))


    def delete_qualification(self, qualification_id: UUID) -> None:
        """Permanently delete a qualification.
        Args:
            qualification_id: ID of qualification to delete
        """
        try:
            self.repository.delete(qualification_id)
        except EntityNotFoundError as e:
            raise QualificationNotFoundError(id=qualification_id, detail = str(e))
        #Raise relationship errors on deletion


    # Archive factory methods
    def get_all_archived_qualifications(self, filters) -> List[EducatorQualifications]:
        """Get all archived qualifications with filtering.
        Returns:
            List[EducatorQualifications]: List of archived qualification records
        """
        fields = ['name', 'description']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_qualification(self, qualification_id: UUID) -> EducatorQualifications:
        """Get a specific archived qualification by ID.
        Args:
            qualification_id: ID of qualification to retrieve
        Returns:
            EducatorQualifications: Retrieved archived qualification record
        """
        try:
            return self.repository.get_archive_by_id(qualification_id)
        except EntityNotFoundError as e:
            raise QualificationNotFoundError(id=qualification_id, detail = str(e))


    def restore_qualification(self, qualification_id: UUID) -> EducatorQualifications:
        """Restore a qualification.
        Args:
            qualification_id: ID of qualification to restore
        Returns:
            EducatorQualifications: Restore qualification record
        """
        try:
            archived = self.get_archived_qualification(qualification_id)
            archived.last_modified_by = SYSTEM_USER_ID
            return self.repository.restore(qualification_id)
        except EntityNotFoundError as e:
            raise QualificationNotFoundError(id=qualification_id, detail = str(e))


    def delete_archived_qualification(self, qualification_id: UUID) -> None:
        """Permanently delete an archived qualification.
        Args:
            qualification_id: ID of qualification to delete
        """
        try:
            self.repository.delete_archive(qualification_id)
        except EntityNotFoundError as e:
            raise QualificationNotFoundError(id=qualification_id, detail = str(e))