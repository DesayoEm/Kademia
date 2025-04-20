from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from V2.app.core.shared.services.export_service import ExportService
from V2.app.core.shared.services.lifecycle_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service import DeleteService
from ....core.validators.staff_organization import StaffOrganizationValidator
from ....core.validators.entity_validators import EntityValidator
from V2.app.database.models.staff_organization import StaffDepartment
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository

from V2.app.core.shared.errors.fk_resolver import FKResolver
from ....core.errors.maps.error_map import error_map
from ....core.errors.maps.fk_mapper import fk_error_map
from V2.app.core.shared.errors import (
    DuplicateEntityError, ArchiveDependencyError, EntityNotFoundError, UniqueViolationError, RelationshipError
)

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class StaffDepartmentFactory:
    """Factory class for managing staff department operations."""

    def __init__(self, session: Session, model = StaffDepartment):
        """Initialize factory with model and database session.
        Args:
            session: SQLAlchemy database session
            model: Model class, defaults to StaffRole
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.entity_validator = EntityValidator(session)
        self.validator = StaffOrganizationValidator()
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.export_service = ExportService(session)
        self.validator = StaffOrganizationValidator()
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.domain = "Staff department"


    def create_staff_department(self, new_department) -> StaffDepartment:
        """Create a new staff department.
        Args:
            new_department: Department data containing name and description
        Returns:
            StaffDepartment: Created department record
        """
        department = StaffDepartment(
            id=uuid4(),
            name=self.validator.validate_name(new_department.name),
            description=self.validator.validate_description(new_department.description),

            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
        )
        try:
            return self.repository.create(department)


        except UniqueViolationError as e:
            error_message = str(e).lower()
            unique_violation_map = {
                "staff_departments_name_key": ("name", new_department.name)
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
                factory_class=self.__class__, error_message=str(e), context_obj=new_department,
                operation="create", fk_map=fk_error_map
            )
            if resolved:
                raise resolved

            raise RelationshipError(
                error=str(e), operation="create", entity_model="unknown",domain=self.domain
            )

    def get_staff_department(self, department_id: UUID) -> StaffDepartment:
        """Get a specific staff department by ID.
        Args:
            department_id (UUID): ID of department to retrieve
        Returns:
            StaffDepartment: Retrieved department record
        """
        try:
            return self.repository.get_by_id(department_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=department_id, error=str(e),
                display_name=self.display_name
            )


    def get_all_departments(self, filters) -> List[StaffDepartment]:
        """Get all active departments with filtering.
        Returns:
            List[StaffDepartment]: List of active departments
        """
        fields = ['name']
        return self.repository.execute_query(fields, filters)


    def update_staff_department(self, department_id: UUID, data: dict) -> StaffDepartment:
        """Update a staff department's information.
        Args:
            department_id (UUID): ID of department to update
            data (dict): Dictionary containing fields to update
        Returns:
            StaffDepartment: Updated department record
        """
        original = data.copy()

        try:
            existing = self.get_staff_department(department_id)
            validations = {
                "name": (self.validator.validate_name, "name"),
                "description": (self.validator.validate_description, "description"),
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in data:
                    validated_value = validator_func(data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            existing.last_modified_by = SYSTEM_USER_ID
            return self.repository.update(department_id, existing)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=department_id, error=str(e),
                display_name=self.display_name
            )
        except UniqueViolationError as e:
            error_message = str(e).lower()
            unique_violation_map = {
                "staff_departments_name_key": ("name", original.get('name'))
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
                error=str(e), operation="update", entity_model="unknown",domain=self.domain
            )

    def archive_department(self, department_id: UUID, reason) -> StaffDepartment:
        """Archive a staff department if no active dependencies exist.
        Args:
            department_id (UUID): ID of department to archive
            reason: Reason for archiving
        Returns:
            StaffDepartment: Archived department record
        """
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=department_id
            )

            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.model, identifier=department_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )

            return self.repository.archive(department_id, SYSTEM_USER_ID, reason)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=department_id, error=str(e),
                display_name=self.display_name
            )

    def delete_department(self, department_id: UUID, is_archived = False) -> None:
        """Permanently delete a staff department if there are no dependent entities.
        Args:
            department_id (UUID): ID of department to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, department_id, is_archived)
            return self.repository.delete(department_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=department_id, error=str(e),
                display_name=self.display_name
            )

        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model='unknown_entity', domain=self.domain)

    def get_all_archived_departments(self, filters) -> List[StaffDepartment]:
        """Get all archived departments with filtering.
        Returns:
            List[StaffDepartment]: List of archived department records
        """
        fields = ['name']
        return self.repository.execute_archive_query(fields, filters)

    def get_archived_department(self, department_id: UUID) -> StaffDepartment:
        """Get an archived department by ID.
        Args:
            department_id: ID of department to retrieve
        Returns:
            StaffDepartment: Retrieved department record
        """
        try:
            return self.repository.get_archive_by_id(department_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=department_id, error=str(e),
                display_name=self.display_name
            )

    def restore_department(self, department_id: UUID) -> StaffDepartment:
        """Restore an archived department.
        Args:
            department_id: ID of department to restore
        Returns:
            StaffDepartment: Restored department record
        """
        try:
            return self.repository.restore(department_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=department_id, error=str(e),
                display_name=self.display_name
            )

    def delete_archived_department(self, department_id: UUID, is_archived = True) -> None:
        """Permanently delete an archived department if there are no dependent entities.
        Args:
            department_id: ID of department to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, department_id, is_archived)
            self.repository.delete_archive(department_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=department_id, error=str(e),
                display_name=self.display_name
            )

        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model='unknown_entity', domain = self.domain)

