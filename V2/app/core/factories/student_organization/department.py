from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from ...errors.fk_resolver import FKResolver
from ...services.lifecycle_service.archive_service import ArchiveService
from ...services.lifecycle_service.delete_service import DeleteService
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....core.validators.student_organization import StudentOrganizationValidator
from ....database.models.student_organization import StudentDepartment

from ....core.errors.maps.error_map import error_map
from ....core.errors.maps.fk_mapper import fk_error_map
from ...errors import (
    DuplicateEntityError, ArchiveDependencyError, EntityNotFoundError, UniqueViolationError, RelationshipError
)


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')

class StudentDepartmentFactory:
    """Factory class for managing student department operations."""

    def __init__(self, session: Session, model = StudentDepartment):
        """Initialize factory with database session.
        Args:
            session: SQLAlchemy database session
            model: Model class, defaults to StudentDepartment
        """
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = StudentOrganizationValidator()
        self.repository = SQLAlchemyRepository(self.model, session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.domain = "Student department"


    def create_student_department(self, new_department) -> StudentDepartment:
        """Create a new student department.
        Args:
            new_department: Department data containing name and description
        Returns:
            StudentDepartment: Created department record
        """
        department = StudentDepartment(
            id = uuid4(),
            name = self.validator.validate_name(new_department.name),
            description=self.validator.validate_description(new_department.description),
            code=self.validator.validate_code(new_department.code),

            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID
        )
        try:
            return self.repository.create(department)

        except UniqueViolationError as e:
            error_message = str(e).lower()

            unique_violation_map = {
                "student_departments_name_key": ("name", new_department.name),
                "student_departments_code_key": ("code", str(new_department.code.value)),
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
                    error=str(e), operation="create", entity_model="unknown", domain=self.domain
                )


    def get_student_department(self, department_id: UUID) -> StudentDepartment:
        """Get a specific student department by ID.
        Args:
            department_id (UUID): ID of department to retrieve
        Returns:
            StudentDepartment: Retrieved department record
        """
        try:
            return self.repository.get_by_id(department_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=department_id, error=str(e),
                display_name=self.display_name
            )


    def get_all_departments(self, filters) -> List[StudentDepartment]:
        """Get all active departments with filtering.
        Returns:
            List[StudentDepartment]: List of active departments
        """
        fields = ['name']
        return self.repository.execute_query(fields, filters)


    def update_student_department(self, department_id: UUID, data: dict) -> StudentDepartment:
        """Update a student department's information.
        Args:
            department_id (UUID): ID of department to update
            data (dict): Dictionary containing fields to update
        Returns:
            StudentDepartment: Updated department record
        """
        try:
            existing = self.get_student_department(department_id)

            validations = {
                "name": (self.validator.validate_level_name, "name"),
                "description": (self.validator.validate_description, "description"),
                "code": (self.validator.validate_code, "code")
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
                "student_departments_name_key": ("name", data.get('name')),
                "student_departments_code_key": ("code", data.get('code')),
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


    def archive_department(self, department_id: UUID, reason) -> StudentDepartment:
        """Archive a student department if no active dependencies exist.
        Args:
            department_id (UUID): ID of department to archive
            reason: Reason for archiving
        Returns:
            StudentDepartment: Archived department record
        """
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=department_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=department_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )

            return self.repository.archive(department_id, SYSTEM_USER_ID, reason)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=department_id, error=str(e),
                display_name=self.display_name
            )


    def delete_department(self, department_id: UUID, is_archived = False) -> None:
        """Permanently delete a student department if there are no dependent entities.
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
                error=str(e), operation='delete', entity_model=self.model.__name__, domain = self.domain
            )


    def get_all_archived_departments(self, filters) -> List[StudentDepartment]:
        """Get all archived departments with filtering.
        Returns:
            List[StudentDepartment]: List of archived department records
        """
        fields = ['name']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_department(self, department_id: UUID) -> StudentDepartment:
        """Get an archived department by ID.
        Args:
            department_id: ID of department to retrieve
        Returns:
            StudentDepartment: Retrieved department record
        """
        try:
            return self.repository.get_archive_by_id(department_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=department_id, error=str(e),
                display_name=self.display_name
            )


    def restore_department(self, department_id: UUID) -> StudentDepartment:
        """Restore an archived department.
        Args:
            department_id: ID of department to restore
        Returns:
            StudentDepartment: Restored department record
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
                error=str(e), operation='delete', entity_model=self.model.__name__, domain = self.domain
            )




