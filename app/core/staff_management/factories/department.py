from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.services.audit_export_service.export import ExportService
from app.core.staff_management.services.validators import StaffManagementValidator
from app.core.staff_management.models import StaffDepartment
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from app.core.shared.exceptions.maps.error_map import error_map



class StaffDepartmentFactory(BaseFactory):
    """Factory class for managing staff department operations."""

    def __init__(self, session: Session, model = StaffDepartment, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session, model and current user.
        Args:
            session: SQLAlchemy db session
            model: Model class, defaults to StaffDepartment
            current_user: The authenticated user performing the operation, if any.
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = StaffManagementValidator()
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.export_service = ExportService(session)
        self.validator = StaffManagementValidator()
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Staff department"


    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_fk_on_create()
    @resolve_unique_violation({
        "staff_departments_name_key": ("name", lambda self, data: data.name),
    })
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

            created_by=self.get_actor_id(),
            last_modified_by=self.get_actor_id(),
        )
        return self.repository.create(department)


    def get_all_departments(self, filters) -> List[StaffDepartment]:
        """Get all active departments with filtering.
        Returns:
            List[StaffDepartment]: List of active departments
        """
        fields = ['name']
        return self.repository.execute_query(fields, filters)


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
            self.raise_not_found(department_id, e)


    @resolve_fk_on_update()
    @resolve_unique_violation({
        "staff_departments_name_key": ("name", lambda self, *a: a[-1].get("name")),
    })
    def update_staff_department(self, department_id: UUID, data: dict) -> StaffDepartment:
        """Update a staff department's information.
        Args:
            department_id (UUID): ID of department to update
            data (dict): Dictionary containing fields to update
        Returns:
            StaffDepartment: Updated department record
        """
        copied_data = data.copy()
        try:
            existing = self.get_staff_department(department_id)
            validations = {
                "name": (self.validator.validate_name, "name"),
                "description": (self.validator.validate_description, "description"),
            }
            #leave original data untouched for error message extraction
            for field, (validator_func, model_attr) in validations.items():
                if field in copied_data:
                    validated_value = validator_func(copied_data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in copied_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            existing.last_modified_by = self.get_actor_id()
            return self.repository.update(department_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(department_id, e)


    def archive_department(self, department_id: UUID, reason) -> StaffDepartment:
        """Archive a staff department if no active staff members are assigned to it."""
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
            return self.repository.archive(department_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(department_id, e)


    @resolve_fk_on_delete()
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
            self.raise_not_found(department_id, e)


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
            self.raise_not_found(department_id, e)


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
            self.raise_not_found(department_id, e)


    @resolve_fk_on_delete()
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
            self.raise_not_found(department_id, e)

