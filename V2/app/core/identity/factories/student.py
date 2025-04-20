from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from V2.app.core.identity.services.student_service import StudentService
from V2.app.core.auth.services.password_service import PasswordService
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.core.shared.database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.identity.validators.identity import IdentityValidator
from V2.app.core.shared.database.models import Student
from ...shared.errors.maps.error_map import error_map
from ...shared.errors import ArchiveDependencyError, EntityNotFoundError, StaffTypeError
from ...shared.errors.decorators.resolve_unique_violation import resolve_unique_violation
from ...shared.errors.decorators.resolve_fk_violation import (
    resolve_fk_on_update, resolve_fk_on_create, resolve_fk_on_delete
)


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class StudentFactory:
    """Factory class for managing student operations."""

    def __init__(self, session: Session, model=Student):
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = IdentityValidator()
        self.password_service = PasswordService(session)
        self.student_service = StudentService(session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.domain = "Student"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_unique_violation({
        "students_student_id_key": ("student ID", lambda self, student_data: self.student_service.generate_student_id(student_data.session_start_year))
    })
    @resolve_fk_on_create()
    def create_student(self, student_data) -> Student:
        password = student_data.last_name.title()

        new_student = Student(
            id=uuid4(),
            first_name=self.validator.validate_name(student_data.first_name),
            last_name=self.validator.validate_name(student_data.last_name),
            password_hash=self.password_service.hash_password(password),
            guardian_id=student_data.guardian_id,
            session_start_year=self.validator.validate_session_start_year(student_data.session_start_year),
            student_id=self.student_service.generate_student_id(student_data.session_start_year),
            gender=student_data.gender,
            date_of_birth=self.validator.validate_date(student_data.date_of_birth),
            level_id=student_data.level_id,
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
        )
        return self.repository.create(new_student)


    def get_student(self, student_id: UUID) -> Student:
        try:
            return self.repository.get_by_id(student_id)
        except EntityNotFoundError as e:
            self.raise_not_found(student_id, e)


    def get_all_students(self, filters) -> List[Student]:
        fields = ['name', 'student_id']
        return self.repository.execute_query(fields, filters)


    @resolve_fk_on_update()
    def update_student(self, student_id: UUID, data: dict) -> Student:
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

        except EntityNotFoundError as e:
            self.raise_not_found(student_id, e)


    def archive_student(self, student_id: UUID, reason) -> Student:
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
            self.raise_not_found(student_id, e)


    @resolve_fk_on_delete()
    def delete_student(self, student_id: UUID, is_archived=False) -> None:
        try:
            self.delete_service.check_safe_delete(self.model, student_id, is_archived)
            return self.repository.delete(student_id)

        except EntityNotFoundError as e:
            self.raise_not_found(student_id, e)


    def get_all_archived_students(self, filters) -> List[Student]:
        fields = ['name', 'student_id']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_student(self, student_id: UUID) -> Student:
        try:
            return self.repository.get_archive_by_id(student_id)
        except EntityNotFoundError as e:
            self.raise_not_found(student_id, e)


    def restore_student(self, student_id: UUID) -> Student:
        try:
            return self.repository.restore(student_id)

        except EntityNotFoundError as e:
            self.raise_not_found(student_id, e)


    @resolve_fk_on_delete()
    def delete_archived_student(self, student_id: UUID, is_archived=True) -> None:
        try:
            self.delete_service.check_safe_delete(self.model, student_id, is_archived)
            self.repository.delete_archive(student_id)

        except EntityNotFoundError as e:
            self.raise_not_found(student_id, e)