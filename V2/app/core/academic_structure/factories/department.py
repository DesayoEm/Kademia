
from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.core.academic_structure.models import StudentDepartment
from V2.app.core.academic_structure.services.validators import AcademicStructureValidator
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from V2.app.core.shared.exceptions import EntityNotFoundError, ArchiveDependencyError
from V2.app.core.shared.exceptions.maps.error_map import error_map


class StudentDepartmentFactory(BaseFactory):
    """Factory class for managing student department operations."""

    def __init__(self, session: Session, model=StudentDepartment, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session, model and current actor..
            Args:
                session: SQLAlchemy db session
                model: Model class, defaults to StudentDepartment
                current_user: The authenticated user performing the operation,
        """

        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = AcademicStructureValidator()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Student Department"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_unique_violation({
        "student_departments_name_key": ("name", lambda self, data: data.name),
        "student_departments_code_key": ("code", lambda self, data: data.code),
    })
    @resolve_fk_on_create()
    def create_student_department(self, data) -> StudentDepartment:
        """Create a new student department.
        Args:
            data: Department data containing name and description
        Returns:
            StudentDepartment: Created department record
        """
        department = StudentDepartment(
            id=uuid4(),
            name=self.validator.validate_name(data.name),
            description=self.validator.validate_description(data.description),
            code=self.validator.validate_code(data.code),

            created_by=self.actor_id,
            last_modified_by=self.actor_id,
        )
        return self.repository.create(department)


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
            self.raise_not_found(department_id, e)


    def get_all_student_departments(self, filters) -> List[StudentDepartment]:
        """Get all active departments with filtering.
        Returns:
            List[StudentDepartment]: List of active departments
        """
        fields = ['name']
        return self.repository.execute_query(fields, filters)


    @resolve_fk_on_update()
    @resolve_unique_violation({
        "student_departments_code_key": ("code", lambda self, *a: a[-1].get("code")),
        "student_departments_name_key": ("name", lambda self, *a: a[-1].get("name")),
    })
    def update_student_department(self, department_id: UUID, data: dict) -> StudentDepartment:
        """Update a student department's information.
        Args:
            department_id (UUID): ID of department to update
            data (dict): Dictionary containing fields to update
        Returns:
            StudentDepartment: Updated department record
        """
        original = data.copy()
        try:
            existing = self.get_student_department(department_id)
            validations = {
                "name": (self.validator.validate_name, "name"),
                "description": (self.validator.validate_description, "description"),
                "code": (self.validator.validate_code, "code")
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in data:
                    validated_value = validator_func(original.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(department_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(department_id, e)


    def archive_student_department(self, department_id: UUID, reason) -> StudentDepartment:
        """Archive a student department if no active dependencies exist.
        Args:
            department_id (UUID): ID of department to archive
            reason: Reason for archiving
        Returns:
            StudentDepartment: Archived department record
        """
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                self.model, department_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=department_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(department_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(department_id, e)


    @resolve_fk_on_delete()
    def delete_student_department(self, department_id: UUID, is_archived=False) -> None:
        """Permanently delete a student department if there are no dependent entities.
        Args:
            department_id (UUID): ID of department to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, department_id, is_archived)
            self.repository.delete(department_id)

        except EntityNotFoundError as e:
            self.raise_not_found(department_id, e)


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
            self.raise_not_found(department_id, e)


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
            self.raise_not_found(department_id, e)


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
