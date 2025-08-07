from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.core.shared.factory.base_factory import BaseFactory
from app.core.auth.services.password_service import PasswordService
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.identity.services.validators import IdentityValidator
from app.core.identity.models.student import Student
from ...shared.exceptions.maps.error_map import error_map
from ...shared.exceptions import ArchiveDependencyError, EntityNotFoundError
from ...shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from ...shared.exceptions.decorators.resolve_fk_violation import (
    resolve_fk_on_update, resolve_fk_on_create, resolve_fk_on_delete
)



class StudentFactory(BaseFactory):
    """Factory class for managing student operations."""

    def __init__(self, session: Session, model=Student, current_user = None):
        super().__init__(current_user)
        """Initialize factory with db session, model and current actor.
            Args:
            session: SQLAlchemy db session
            model: Model class, defaults to Student
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = IdentityValidator()
        self.password_service = PasswordService(session)

        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session, current_user)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Student"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_unique_violation({
        "students_student_id_key": ("student ID", lambda self, data: self.student_service.generate_student_id(data.session_start_year))
    })
    @resolve_fk_on_create()
    def create_student(self, student_data) -> Student:
        """Create a new student.
        Args:
            student_data: student data
        Returns:
            student: Created student record
        """
        from app.core.identity.services.student_service import StudentService
        student_service = StudentService(self.session, self.current_user)
        password = student_data.last_name.title()

        new_student = Student(
            id=uuid4(),
            first_name=self.validator.validate_name(student_data.first_name),
            last_name=self.validator.validate_name(student_data.last_name),
            password_hash=self.password_service.hash_password(password),
            guardian_id=student_data.guardian_id,
            session_start_year=self.validator.validate_session_start_year(student_data.session_start_year),
            student_id=student_service.generate_student_id(student_data.session_start_year),
            gender=student_data.gender,
            date_of_birth=self.validator.validate_date(student_data.date_of_birth),
            level_id=student_data.level_id,
            created_by=self.actor_id,
            last_modified_by=self.actor_id,
        )
        return self.repository.create(new_student)


    def get_student(self, student_id: UUID) -> Student:
        """Get a specific student by ID.
        Args:
            student_id (UUID): ID of student to retrieve
        Returns:
            student: Retrieved student record
        """
        try:
            return self.repository.get_by_id(student_id)
        except EntityNotFoundError as e:
            self.raise_not_found(student_id, e)

    def get_all_students(self, filters) -> List[Student]:
        """Get all active student with filtering.
        Returns:
            List[student]: List of active students
        """
        fields = [
            'name', 'student_id', 'level_id', 'department_id', 'is_graduated', 'graduation_year', 'guardian_id'
        ]
        return self.repository.execute_query(fields, filters)


    @resolve_fk_on_update()
    def update_student(self, student_id: UUID, data: dict) -> Student:
        """Update a student profile information.
        Args:
            student_id (UUID): ID of student to update
            data (dict): Dictionary containing fields to update
        Returns:
            student: Updated student record
        """
        copied_data = data.copy()
        try:
            existing = self.get_student(student_id)
            validations = {
                "first_name": (self.validator.validate_name, "first_name"),
                "last_name": (self.validator.validate_name, "last_name"),
                "date_of_birth": (self.validator.validate_date, "date_of_birth"),
                "session_start_year": (self.validator.validate_session_start_year, "session_start_year"),
            }
            # leave original data untouched for error message extraction
            for field, (validator_func, model_attr) in validations.items():
                if field in copied_data:
                    validated_value = validator_func(copied_data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in copied_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            existing.last_modified_by = self.actor_id
            return self.repository.update(student_id, existing)

        except EntityNotFoundError as e:
            self.raise_not_found(student_id, e)


    def archive_student(self, student_id: UUID, reason) -> Student:
        """Archive student if no active dependencies exist.
        Args:
            student_id (UUID): ID of student to archive
            reason (ArchiveReason): Reason for archiving
        Returns:
            student: Archived student record
        """
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=student_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=student_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(student_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(student_id, e)


    @resolve_fk_on_delete()
    def delete_student(self, student_id: UUID, is_archived=False) -> None:
        """Permanently delete a student if there are no dependent entities.
        Args:
            student_id (UUID): ID of student to delete
            is_archived(bool): Whether to check active or archived records
        """
        try:
            self.delete_service.check_safe_delete(self.model, student_id, is_archived)
            return self.repository.delete(student_id)

        except EntityNotFoundError as e:
            self.raise_not_found(student_id, e)


    def get_all_archived_students(self, filters) -> List[Student]:
        """Get all archived student with filtering.
        Returns:
            List[student]: List of archived student records
        """
        fields = [
            'name', 'student_id', 'level_id', 'department_id', 'is_graduated', 'graduation_year', 'guardian_id'
        ]
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_student(self, student_id: UUID) -> Student:
        """Get an archived student by ID.
        Args:
            student_id: ID of student to retrieve
        Returns:
            student: Retrieved student record
        """
        try:
            return self.repository.get_archive_by_id(student_id)
        except EntityNotFoundError as e:
            self.raise_not_found(student_id, e)


    def restore_student(self, student_id: UUID) -> Student:
        """Restore an archived student.
        Args:
            student_id: ID of student to restore
        Returns:
            student: Restored student record
        """
        try:
            return self.repository.restore(student_id)

        except EntityNotFoundError as e:
            self.raise_not_found(student_id, e)


    @resolve_fk_on_delete()
    def delete_archived_student(self, student_id: UUID, is_archived=True) -> None:
        """Permanently delete an archived student.
        Args:
            student_id: ID of student to delete
            is_archived(bool): Whether to check active or archived records
        """
        try:
            self.delete_service.check_safe_delete(self.model, student_id, is_archived)
            self.repository.delete_archive(student_id)

        except EntityNotFoundError as e:
            self.raise_not_found(student_id, e)