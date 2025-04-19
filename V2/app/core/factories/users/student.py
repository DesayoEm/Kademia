from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from ...services.auth.password_service import PasswordService
from ...services.lifecycle_service.archive_service import ArchiveService
from ...services.lifecycle_service.delete_service import DeleteService
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....core.validators.users import UserValidator
from ....core.services.users.student_service import StudentService
from ....database.models.users import Student

from ...errors.fk_resolver import FKResolver
from ....core.errors.maps.error_map import error_map
from ....core.errors.maps.fk_mapper import fk_error_map
from ...errors import (
    DuplicateEntityError, ArchiveDependencyError, EntityNotFoundError, UniqueViolationError,
    RelationshipError,StaffTypeError
)


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class StudentFactory:
    """Factory class for managing student operations."""

    def __init__(self, session: Session, model=Student):
        """Initialize factory with model and database session.
            Args:
            session: SQLAlchemy database session
            model: Model class, defaults to Student
        """

        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = UserValidator()
        self.password_service = PasswordService(session)
        self.student_service = StudentService(session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.domain = "Student"


    def create_student(self, student_data) -> Student:
        """Create a new student.
        Args:
            student_data: student data
        Returns:
            student: Created student record
        """
        password = student_data.last_name.title()
        new_student = Student(
            id=uuid4(),
            first_name=self.validator.validate_name(student_data.first_name),
            last_name=self.validator.validate_name(student_data.last_name),
            password_hash=self.password_service.hash_password(password),
            guardian_id=student_data.guardian_id,
            session_start_year=self.validator.validate_session_start_year(student_data.session_start_year),
            student_id = self.student_service.generate_student_id(student_data.session_start_year),
            gender=student_data.gender,
            date_of_birth = self.validator.validate_date(student_data.date_of_birth),#Think. does student DOB need more constraints
            level_id=student_data.level_id,

            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
        )
        try:
            return self.repository.create(new_student)

        except UniqueViolationError as e:
            error_message = str(e).lower()
            unique_violation_map = {
                "students_student_id_key": ("student ID", new_student.student_id),
            }

            for constraint_key, (field_name, entry_value) in unique_violation_map.items():
                if constraint_key in error_message:
                    raise DuplicateEntityError(
                        entity_model=self.entity_model, entry=entry_value, field=field_name,
                        display_name=self.display_name, detail=error_message
                    )

        except RelationshipError as e:
            resolved = FKResolver.resolve_fk_violation(
                factory_class=self.__class__, error_message=str(e), context_obj=new_student,
                operation="create", fk_map=fk_error_map
            )

            if resolved:
                raise resolved
            raise RelationshipError(
                error=str(e), operation="create", entity_model="unknown", domain=self.domain
            )


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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=student_id, error=str(e),
                display_name=self.display_name
            )


    def get_all_students(self, filters) -> List[Student]:
        """Get all active student with filtering.
        Returns:
            List[student]: List of active students
        """
        fields = ['name', 'student_id']
        return self.repository.execute_query(fields, filters)


    def update_student(self, student_id: UUID, data: dict) -> Student:
        """Update a student profile information.
        Args:
            student_id (UUID): ID of student to update
            data (dict): Dictionary containing fields to update
        Returns:
            student: Updated student record
        """
        original = data.copy()
        try:
            existing = self.get_student(student_id)

            validations = {
                "first_name": (self.validator.validate_name, "first_name"),
                "last_name": (self.validator.validate_name, "last_name"),
                "date_of_birth": (self.validator.validate_date, "date_of_birth"),
                "session_start_year": (self.validator.validate_session_start_year, "session_start_year"),
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in data:
                    validated_value = validator_func(data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            existing.last_modified_by = SYSTEM_USER_ID
            return self.repository.update(student_id, existing)

        except UniqueViolationError as e:
            raise DuplicateEntityError(
                entity_model=self.entity_model, entry="unknown", field='unknown',
                display_name="unknown", detail=str(e))

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


    def archive_student(self, student_id: UUID, reason) -> Student:
            """Archive student if no active dependencies exist.
            Args:
                student_id (UUID): ID of student to archive
                reason: Reason for archiving
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

                return self.repository.archive(student_id, SYSTEM_USER_ID, reason)

            except EntityNotFoundError as e:
                raise EntityNotFoundError(
                    entity_model=self.entity_model, identifier=student_id, error=str(e),
                    display_name=self.display_name
                )


    def delete_student(self, student_id: UUID, is_archived = False) -> None:
        """Permanently delete a student.
        Args:
            student_id (UUID): ID of student to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, student_id, is_archived)
            return self.repository.delete(student_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=student_id, error=str(e),
                display_name=self.display_name
            )
        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model=self.model.__name__, domain = self.domain
            )


    def get_all_archived_students(self, filters) -> List[Student]:
        """Get all archived student with filtering.
        Returns:
            List[student]: List of archived student records
        """
        fields = ['name', 'student_id']
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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=student_id, error=str(e),
                display_name=self.display_name

            )

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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=student_id, error=str(e),
                display_name=self.display_name
            )


    def delete_archived_student(self, student_id: UUID, is_archived = True) -> None:
        """Permanently delete an archived student.
        Args:
            student_id: ID of student to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, student_id, is_archived)
            self.repository.delete_archive(student_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=student_id, error=str(e),
                display_name=self.display_name
            )

        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model=self.model.__name__, domain=self.domain
            )


