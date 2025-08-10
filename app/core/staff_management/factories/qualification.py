from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.services.audit_export_service.export import ExportService
from app.core.staff_management.services.validators import StaffManagementValidator
from app.core.staff_management.models import EducatorQualification
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from app.core.shared.exceptions import EntityNotFoundError
from app.core.shared.exceptions.maps.error_map import error_map


class QualificationFactory(BaseFactory):
    """Factory class for managing qualification operations."""

    def __init__(self, session: Session, model = EducatorQualification, current_user = None):
        super().__init__(current_user)
        """Initialize factory with model and db session.
        Args:
            session: SQLAlchemy db session
            model: Model class, defaults to EducatorQualification
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session, current_user)
        self.export_service = ExportService(session)
        self.validator = StaffManagementValidator()
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Educator Qualification"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_unique_violation({
        "uq_educator_qualification_name": ("name", lambda self,_, data: data.name)
                })

    @resolve_fk_on_create()
    def create_qualification(self, educator_id: UUID, data) -> EducatorQualification:
        """Create a new qualification.
        Args:
            educator_id: id of educator to create qualification for
            data: Qualification data containing name, description and owner
        Returns:
            EducatorQualification: Created qualification record
        """
        qualification = EducatorQualification(
            id=uuid4(),
            educator_id=educator_id,
            name=self.validator.validate_name(data.name),
            description=self.validator.validate_description(data.description),
            validity_type = data.validity_type,
            valid_until = self.validator.validate_valid_until(
                data.validity_type.value,
                data.valid_until
            ),
            created_by=self.actor_id,
            last_modified_by=self.actor_id,
        )
        return self.repository.create(qualification)


    def get_all_qualifications(self, filters) -> List[EducatorQualification]:
        """Get all active qualifications with filtering.
        Returns:
            List[EducatorQualification]: List of active qualification records
        """
        fields = ['name', 'educator_id', 'is_expired', 'validity_type']
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
            self.raise_not_found(qualification_id, e)


    @resolve_fk_on_update()
    @resolve_unique_violation({
        "uq_educator_qualification_name": ("name", lambda self, _, data: data.name)
    })
    def update_qualification(self, qualification_id: UUID, data: dict) -> EducatorQualification:
        """Update a qualification's information.
        Args:
            qualification_id: ID of qualification to update
            data: Dictionary containing fields to update
        Returns:
            EducatorQualification: Updated qualification record
        """
        copied_data = data.copy()
        try:
            existing = self.get_qualification(qualification_id)
            educator_id = existing.educator_id  # stored for for error handling

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
            # leave original data untouched for error message extraction
            for field, (validator_func, model_attr) in validations.items():
                if field in copied_data:
                    validated_value = validator_func(copied_data.pop(field))
                    setattr(existing, model_attr, validated_value)

            return self.repository.update(qualification_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(qualification_id, e)


    def archive_qualification(self, qualification_id: UUID, reason) -> EducatorQualification:
        """Archive a qualification.
        Args:
            qualification_id: ID of qualification to archive
            reason: Reason for archiving
        Returns:
            EducatorQualification: Archived qualification record
        """
        try:
            return self.repository.archive(qualification_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(qualification_id, e)


    @resolve_fk_on_delete()
    def delete_qualification(self, qualification_id: UUID) -> None:
        """Permanently delete a qualification.
        Args:
            qualification_id: ID of qualification to delete
        """
        try:
            self.repository.delete(qualification_id)
        except EntityNotFoundError as e:
            self.raise_not_found(qualification_id, e)


    # Archive factory methods
    def get_all_archived_qualifications(self, filters) -> List[EducatorQualification]:
        """Get all archived qualifications with filtering.
        Returns:
            List[EducatorQualification]: List of archived qualification records
        """
        fields = ['name', 'educator_id', 'is_expired', 'validity_type']
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
            self.raise_not_found(qualification_id, e)


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
            self.raise_not_found(qualification_id, e)


    @resolve_fk_on_delete()
    def delete_archived_qualification(self, qualification_id: UUID) -> None:
        """Permanently delete an archived qualification.
        Args:
            qualification_id: ID of qualification to delete
        """
        try:
            self.repository.delete_archive(qualification_id)
        except EntityNotFoundError as e:
            self.raise_not_found(qualification_id, e)