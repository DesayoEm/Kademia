from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from ...errors.student_organisation_errors import(
RelatedLevelNotFoundError, RelatedClassNotFoundError,
RelatedStudentDepartmentNotFoundError as RelatedDepartmentNotFoundError,
    )
from ....core.errors.database_errors import (
    RelationshipError, UniqueViolationError,EntityNotFoundError
    )
from ...errors.user_profile_errors import (
    DuplicateStudentIDError, DuplicateStudentError, RelatedGuardianNotFoundError, StudentNotFoundError
)
from ...services.auth.password_service import PasswordService
from ....database.db_repositories.sqlalchemy_repos.main_repo import SQLAlchemyRepository
from ....database.models.enums import ArchiveReason
from ....core.validators.users import UserValidator
from ....core.services.users.student_service import StudentService
from ....database.models.users import Student

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class StudentFactory:
    """Factory class for managing student operations."""

    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(Student, session)
        self.validator = UserValidator()
        self.password_service = PasswordService()
        self.student_service = StudentService(session)


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
            class_id=student_data.class_id,
            department_id=student_data.department_id,
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
        )
        try:
            return self.repository.create(new_student)
        except UniqueViolationError as e:
            error_message = str(e).lower()
            if "students_student_id_key" in error_message:
                raise DuplicateStudentIDError(
                    stu_id=new_student.student_id, detail=error_message
                )
            else:
                raise DuplicateStudentError(
                    input_value="unknown field",detail=error_message)
        except RelationshipError as e:
            error_message = str(e)
            fk_error_mapping = {
                'fk_students_guardians_guardian_id': ('guardian_id', RelatedGuardianNotFoundError),
                'fk_students_academic_levels_level_id': ('level_id', RelatedLevelNotFoundError),
                'fk_students_classes_class_id': ('class_id', RelatedClassNotFoundError),
                'fk_students_student_departments_department_id': ('department_id', RelatedDepartmentNotFoundError),
            }
            for fk_constraint, (attr_name, error_class) in fk_error_mapping.items():
                if fk_constraint in error_message:
                    entity_id = getattr(student_data, attr_name, None)
                    if entity_id:
                        raise error_class(id=entity_id, detail=error_message, action='create')

            raise RelationshipError(error=error_message, operation='create', entity='unknown_entity')


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
            raise StudentNotFoundError(id=student_id, detail = str(e))


    def get_all_students(self, filters) -> List[Student]:
        """Get all active student with filtering.
        Returns:
            List[student]: List of active students
        """
        fields = ['first_name','last_name', 'student_id']
        return self.repository.execute_query(fields, filters)


    def update_student(self, student_id: UUID, data: dict) -> Student:
        """Update a student profile information.
        Args:
            student_id (UUID): ID of student to update
            data (dict): Dictionary containing fields to update
        Returns:
            student: Updated student record
        """
        try:
            existing = self.get_student(student_id)

            if 'first_name' in data:
                existing.first_name = self.validator.validate_name(data.pop('first_name'))
            if 'last_name' in data:
                existing.last_name = self.validator.validate_name(data.pop('last_name'))
            if 'date_of_birth' in data:
                existing.date_of_birth = self.validator.validate_date(data.pop('date_of_birth'))
            if 'session_start_year' in data:
                existing.session_start_year = self.validator.validate_session_start_year(data.pop('session_start_year'))

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            existing.last_modified_by = SYSTEM_USER_ID
            return self.repository.update(student_id, existing)

        except UniqueViolationError as e:
            raise DuplicateStudentError(input_value="unknown",  detail=str(e))

        except RelationshipError as e:
            raise RelationshipError(error=str(e), operation='update', entity='unknown')


    def archive_student(self, student_id: UUID, reason: ArchiveReason) -> Student:
            """Archive student.
            Args:
                student_id (UUID): ID of student to archive
                reason (ArchiveReason): Reason for archiving
            Returns:
                student: Archived student record
            """
            try:
                return self.repository.archive(student_id, SYSTEM_USER_ID, reason)
            except EntityNotFoundError as e:
                raise StudentNotFoundError(id=student_id, detail = str(e))


    def delete_student(self, student_id: UUID) -> None:
        """Permanently delete a student.
        Args:
            student_id (UUID): ID of student to delete
        """
        try:
            self.repository.delete(student_id)
        except EntityNotFoundError as e:
            raise StudentNotFoundError(id=student_id, detail = str(e))


    def get_all_archived_students(self, filters) -> List[Student]:
        """Get all archived student with filtering.
        Returns:
            List[student]: List of archived student records
        """
        fields = ['first_name','last_name', 'student_id']
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
            raise StudentNotFoundError(id=student_id, detail = str(e))

    def restore_student(self, student_id: UUID) -> Student:
        """Restore an archived student.
        Args:
            student_id: ID of student to restore
        Returns:
            student: Restored student record
        """
        try:
            archived = self.get_archived_student(student_id)
            archived.last_modified_by = SYSTEM_USER_ID
            return self.repository.restore(student_id)
        except EntityNotFoundError as e:
            raise StudentNotFoundError(id=student_id, detail = str(e))


    def delete_archived_student(self, student_id: UUID) -> None:
        """Permanently delete an archived student.
        Args:
            student_id: ID of student to delete
        """
        try:
            self.repository.delete_archive(student_id)
        except EntityNotFoundError as e:
            raise StudentNotFoundError(id=student_id, detail = str(e))




