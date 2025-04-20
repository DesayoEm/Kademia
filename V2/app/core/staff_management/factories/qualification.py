from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session
from V2.app.core.shared.services.export_service import ExportService
from V2.app.core.shared.services.lifecycle_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service import DeleteService
from ....core.validators.staff_organization import StaffOrganizationValidator

from V2.app.database.models.staff_organization import EducatorQualification
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository

from V2.app.core.shared.errors.fk_resolver import FKResolver
from ....core.errors.maps.error_map import error_map
from ....core.errors.maps.fk_mapper import fk_error_map
from V2.app.core.shared.errors import (
    DuplicateEntityError, EntityNotFoundError, UniqueViolationError, RelationshipError
)


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class QualificationFactory:
    """Factory class for managing qualification operations."""

    def __init__(self, session: Session, model = EducatorQualification):
        """Initialize factory with model and database session.
        Args:
            session: SQLAlchemy database session
            model: Model class, defaults to EducatorQualification
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.export_service = ExportService(session)
        self.validator = StaffOrganizationValidator()
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.domain = "Educator Qualification"


    def create_qualification(self, new_qualification) -> EducatorQualification:
        """Create a new qualification.
        Args:
            new_qualification: Qualification data containing name, description and owner
        Returns:
            EducatorQualification: Created qualification record
        """
        qualification = EducatorQualification(
            id=uuid4(),
            educator_id=new_qualification.educator_id,
            name=self.validator.validate_name(new_qualification.name),
            description=self.validator.validate_description(new_qualification.description),
            validity_type = new_qualification.validity_type,

            valid_until = self.validator.validate_valid_until(new_qualification.validity_type.value,
                                    new_qualification.valid_until),

            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
        )
        try:
            return self.repository.create(qualification)

        except UniqueViolationError as e:
            error_message = str(e)
            unique_violation_map = {
                "uq_educator_qualification_name": ("name", new_qualification.name),
            }
            for constraint_key, (field_name, entry_value) in unique_violation_map.items():
                if constraint_key in error_message:
                    raise DuplicateEntityError(
                        entity_model=self.entity_model, entry=entry_value, field=field_name,
                        display_name=self.display_name, detail=error_message
                    )
            raise DuplicateEntityError(
                entity_model=self.entity_model, entry="unknown", field='unknown',
                display_name="unknown", detail=error_message)

        except RelationshipError as e:
            resolved = FKResolver.resolve_fk_violation(
                factory_class=self.__class__, error_message=str(e), context_obj=new_qualification,
                operation="create", fk_map=fk_error_map
            )
            if resolved:
                raise resolved
            raise RelationshipError(
                error=str(e), operation="create", entity_model="unknown", domain=self.domain
            )


    def get_all_qualifications(self, filters) -> List[EducatorQualification]:
        """Get all active qualifications with filtering.
        Returns:
            List[EducatorQualification]: List of active qualification records
        """
        fields = ['name']
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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=qualification_id, error=str(e),
                display_name=self.display_name

            )


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
            educator_id = existing.educator_id  # separately stored for for error handling

            if "validity_type" in data and "valid_until" in data:
                existing.validity_type = data['validity_type']

                existing.valid_until = self.validator.validate_valid_until(
                    data['validity_type'], data['valid_until'])

            elif "valid_until" in data:
                existing.valid_until = self.validator.validate_valid_until(
                    existing.validity_type, data['valid_until'])

            elif "validity_type" in data:
                existing.valid_until = self.validator.validate_valid_until(
                    data['validity_type'], existing.valid_until
                )

            validations = {
                "name": (self.validator.validate_name, "name"),
                "description": (self.validator.validate_description, "description"),
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in data:
                    validated_value = validator_func(data.pop(field))
                    setattr(existing, model_attr, validated_value)

            existing.last_modified_by = SYSTEM_USER_ID

            return self.repository.update(qualification_id, existing)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=qualification_id, error=str(e),
                display_name=self.display_name
            )

        except UniqueViolationError as e:
            error_message = str(e)
            unique_violation_map = {
                "uq_educator_qualification_name": ("name",original.get('name', 'unknown')),
            }
            for constraint_key, (field_name, entry_value) in unique_violation_map.items():
                if constraint_key in error_message:
                    raise DuplicateEntityError(
                        entity_model=self.entity_model, entry=entry_value, field=field_name,
                        display_name=self.display_name, detail=error_message
                    )
            raise DuplicateEntityError(
                entity_model=self.entity_model, entry="unknown", field='unknown',
                display_name="unknown", detail=error_message)

        except RelationshipError as e:
            resolved = FKResolver.resolve_fk_violation(
                factory_class=self.__class__, error_message=str(e), context_obj=existing,
                operation="update", fk_map=fk_error_map
            )
            if resolved:
                raise resolved
            raise RelationshipError(
                error=str(e), operation="update", entity_model="unknown", domain=self.domain
            )


    def archive_qualification(self, qualification_id: UUID, reason) -> EducatorQualification:
        """Archive a qualification.
        Args:
            qualification_id: ID of qualification to archive
            reason: Reason for archiving
        Returns:
            EducatorQualification: Archived qualification record
        """
        try:
            #There's no need to check for dependent entities before archiving as there are none
            return self.repository.archive(qualification_id, SYSTEM_USER_ID, reason)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=qualification_id, error=str(e),
                display_name=self.display_name
            )


    def delete_qualification(self, qualification_id: UUID) -> None:
        """Permanently delete a qualification.
        Args:
            qualification_id: ID of qualification to delete
        """
        try:
            #There's no need to check for dependent entities before deletion as there are none
            self.repository.delete(qualification_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=qualification_id, error=str(e),
                display_name=self.display_name

            )
        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model='unknown_entity', domain=self.domain)



    # Archive factory methods
    def get_all_archived_qualifications(self, filters) -> List[EducatorQualification]:
        """Get all archived qualifications with filtering.
        Returns:
            List[EducatorQualification]: List of archived qualification records
        """
        fields = ['name']
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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=qualification_id, error=str(e),
                display_name=self.display_name
            )


    def restore_qualification(self, qualification_id: UUID) -> EducatorQualification:
        """Restore a qualification.
        Args:
            qualification_id: ID of qualification to restore
        Returns:
            EducatorQualification: Restore qualification record
        """
        try:
            return self.repository.restore(qualification_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=qualification_id, error=str(e),
                display_name=self.display_name
            )


    def delete_archived_qualification(self, qualification_id: UUID) -> None:
        """Permanently delete an archived qualification.
        Args:
            qualification_id: ID of qualification to delete
        """
        try:
            # There's no need to check for dependent entities before deletion as there are none
            self.repository.delete_archive(qualification_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=qualification_id, error=str(e),
                display_name=self.display_name
            )
        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model='unknown_entity', domain=self.domain)