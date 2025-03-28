from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from ....core.errors.user_profile_errors import RelatedEducatorNotFoundError
from ....core.validators.staff_organization import StaffOrganizationValidator
from ....database.models.staff_organization import EducatorQualification
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....database.models.enums import ArchiveReason
from ....core.errors.database_errors import (
    EntityNotFoundError, UniqueViolationError, RelationshipError)
from ....core.errors.staff_organisation_errors import QualificationNotFoundError, DuplicateQualificationError


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class QualificationFactory:
    """Factory class for managing qualification operations."""

    def __init__(self, session: Session):
        """Initialize factory with database session.
        Args:
            session: SQLAlchemy database session
        """
        self.repository = SQLAlchemyRepository(EducatorQualification, session)
        self.validator = StaffOrganizationValidator()

    def create_qualification(self, new_qualification) -> EducatorQualification:
        """Create a new qualification.
        Args:
            new_qualification: Qualification data containing name, description and owner
        Returns:
            EducatorQualification: Created qualification record
        """
        qualification = EducatorQualification(
            id=uuid4(),
            name=self.validator.validate_name(new_qualification.name),
            description=self.validator.validate_name(new_qualification.description),
            educator_id=new_qualification.educator_id,
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
                'fk_educator_qualifications_educators_educator_id': ('educator_id', RelatedEducatorNotFoundError),
            }
            for fk_constraint, (attr_name, error_class) in fk_error_mapping.items():
                if fk_constraint in error_message:
                    entity_id = getattr(new_qualification, attr_name, None)
                    if entity_id:
                        raise error_class(id=entity_id, detail=error_message, action='create')

            raise RelationshipError(error=error_message, operation='create', entity='unknown_entity')


    def get_all_qualifications(self, filters) -> List[EducatorQualification]:
        """Get all active qualifications with filtering.
        Returns:
            List[EducatorQualification]: List of active qualification records
        """
        fields = ['name', 'description']
        return self.repository.execute_query(fields, filters)


    def get_qualification(self, qualification_id: UUID) -> EducatorQualification:
        """Get a specific qualification by ID.
        Args:
            qualification_id: ID of qualification to retrieve
        Returns:
            EducatorQualification: Retrieved qualification record
        """
        try:
            return self.repository.get_by_id(qualification_id)
        except EntityNotFoundError as e:
            error_message = str(e)
            raise QualificationNotFoundError(id=qualification_id, detail = error_message)

    def update_qualification(self, qualification_id: UUID, data: dict) -> EducatorQualification:
        """Update a qualification's information.
        Args:
            qualification_id: ID of qualification to update
            data: Dictionary containing fields to update
        Returns:
            EducatorQualification: Updated qualification record
        """
        original = data.copy()
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
                input_value=original.get('name', 'unknown'), detail=str(e), field='name'
            )
        except RelationshipError as e:
            error_message = str(e)
            fk_error_mapping = {
                'fk_educator_qualifications_educators_educator_id': ('educator_id', RelatedEducatorNotFoundError),
            }
            for fk_constraint, (attr_name, error_class) in fk_error_mapping.items():
                if fk_constraint in error_message:
                    entity_id = educator_id
                    if entity_id:
                        raise error_class(id=entity_id, detail=error_message, action='update')

            raise RelationshipError(error=error_message, operation='update', entity='unknown_entity')


    def archive_qualification(self, qualification_id: UUID, reason: ArchiveReason) -> EducatorQualification:
        """Archive a qualification.
        Args:
            qualification_id: ID of qualification to archive
            reason: Reason for archiving
        Returns:
            EducatorQualification: Archived qualification record
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
    def get_all_archived_qualifications(self, filters) -> List[EducatorQualification]:
        """Get all archived qualifications with filtering.
        Returns:
            List[EducatorQualification]: List of archived qualification records
        """
        fields = ['name', 'description']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_qualification(self, qualification_id: UUID) -> EducatorQualification:
        """Get a specific archived qualification by ID.
        Args:
            qualification_id: ID of qualification to retrieve
        Returns:
            EducatorQualification: Retrieved archived qualification record
        """
        try:
            return self.repository.get_archive_by_id(qualification_id)
        except EntityNotFoundError as e:
            raise QualificationNotFoundError(id=qualification_id, detail = str(e))


    def restore_qualification(self, qualification_id: UUID) -> EducatorQualification:
        """Restore a qualification.
        Args:
            qualification_id: ID of qualification to restore
        Returns:
            EducatorQualification: Restore qualification record
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