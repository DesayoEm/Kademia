from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from ...errors.staff_organisation_errors import RelatedRoleNotFoundError, RelatedDepartmentNotFoundError
from ...services.email.onboarding import OnboardingService
from ....core.errors.database_errors import RelationshipError, UniqueViolationError,EntityNotFoundError
from ....core.errors.user_errors import DuplicateStaffError, StaffNotFoundError, StaffTypeError
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....database.models.enums import ArchiveReason
from ....core.validators.users import UserValidator
from ....core.services.auth.password_service import PasswordService
from ....core.validators.entity_validators import EntityValidator
from ....database.models.users import Staff, Educator, SupportStaff, AdminStaff



SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class StaffFactory:
    """Factory class for managing staff operations."""

    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(Staff, session)
        self.validator = UserValidator()
        self.entity_validator = EntityValidator(session)
        self.password_service = PasswordService(session)
        self.onboarding_service = OnboardingService()


    def create_staff(self, staff_data) -> Staff:
        """Create a new staff.
        Args:
            staff_data: staff data
        Returns:
            Staff: Created staff record
        """
        password = self.password_service.generate_random_password()

        def create_staff_instance(data):
            common_attrs = {
                "id": uuid4(),
                "first_name": self.validator.validate_name(data.first_name),
                "last_name": self.validator.validate_name(data.last_name),
                "password_hash": self.password_service.hash_password(password),
                "gender": data.gender,
                "email_address": self.validator.validate_staff_email(data.email_address),
                "address": self.validator.validate_address(data.address),
                "phone": self.validator.validate_phone(data.phone),
                #role and department use error message in entity_validators.py and not the one in the except block.
                "department_id": self.entity_validator.validate_department_exists(data.department_id),
                "role_id": self.entity_validator.validate_role_exists(data.role_id),
                "date_joined": self.validator.validate_date(data.date_joined),
                "created_by": SYSTEM_USER_ID,
                "last_modified_by": SYSTEM_USER_ID,
            }

            if data.staff_type == "Educator":
                return Educator(**common_attrs)
            elif data.staff_type == "Admin":
                return AdminStaff(**common_attrs)
            elif data.staff_type == "Support":
                return SupportStaff(**common_attrs)
            else:
                raise StaffTypeError(
                    valid_types=["Educator", "Admin", "Support"],
                    input_value=data.staff_type
                )
        new_staff = create_staff_instance(staff_data)
        full_name = f"{staff_data.first_name} {staff_data.last_name}"

        try:
            self.onboarding_service.send_staff_onboarding_email(
                staff_data.email_address, full_name, password)
            return self.repository.create(new_staff)

        except UniqueViolationError as e:  #email or phone
            error_message = str(e).lower()
            if "staff_phone_key" in error_message:
                raise DuplicateStaffError(
                    input_value=staff_data.phone, field="phone", detail=error_message)
            elif "staff_email_address_key" in error_message:
                raise DuplicateStaffError(
                    input_value = str(staff_data.email_address), field="email address", detail=error_message)
            else:
                raise DuplicateStaffError(
                    input_value="unknown field", field="unknown", detail=error_message)

        except RelationshipError as e:
            error_message = str(e)
            fk_error_mapping = {
                'Failed to validate role': ('role_id', RelationshipError, 'role'),
                'Failed to validate department': ('department_id', RelationshipError, 'department'),
                #Used hardcoded error messages from entity_validators as SQLAlchemy will not validate fks
                #due to polymorphic association on staff table
                }

            for error, (attr_name, error_class, entity) in fk_error_mapping.items():
                if error in error_message:
                    raise error_class(error=error_message, operation='create', entity=entity)

            raise RelationshipError(error=error_message, operation='create', entity='unknown_entity')


    def get_staff(self, staff_id: UUID) -> Staff:
        """Get a specific staff by ID.
        Args:
            staff_id (UUID): ID of staff to retrieve
        Returns:
            Staff: Retrieved staff record
        """
        try:
            return self.repository.get_by_id(staff_id)

        except EntityNotFoundError as e:
            raise StaffNotFoundError(identifier=staff_id, detail = str(e))


    def get_all_staff(self, filters) -> List[Staff]:
        """Get all active staff with filtering.
        Returns:
            List[Staff]: List of active staffs
        """
        fields = ['name', 'staff_type']
        return self.repository.execute_query(fields, filters)


    def update_staff(self, staff_id: UUID, data: dict) -> Staff:
        """Update a staff profile information.
        Args:
            staff_id (UUID): ID of staff to update
            data (dict): Dictionary containing fields to update
        Returns:
            Staff: Updated staff record
        """
        original = data.copy()
        try:
            existing = self.get_staff(staff_id)
            validations = {
                "first_name": (self.validator.validate_name, "first_name"),
                "last_name": (self.validator.validate_name, "last_name"),
                "email_address": (self.validator.validate_staff_email, "email_address"),
                "phone": (self.validator.validate_phone, "phone"),
                "address": (self.validator.validate_address, "address"),
                "department_id": (self.entity_validator.validate_department_exists, "department_id"),
                "role_id": (self.entity_validator.validate_role_exists, "role_id")
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in data:
                    validated_value = validator_func(data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            existing.last_modified_by = SYSTEM_USER_ID
            return self.repository.update(staff_id, existing)

        except UniqueViolationError as e:
            error_message = str(e).lower()
            if "staff_phone_key" in error_message:
                raise DuplicateStaffError(input_value=original.get('phone', 'unknown'), field="phone", detail=error_message)
            if "staff_email_address_key" in error_message:
                raise DuplicateStaffError(input_value=original.get('email_address', 'unknown'), field="email address",
                                          detail=error_message)
            raise DuplicateStaffError(input_value="unknown field", field="unknown", detail=error_message)


        except RelationshipError as e:
            error_message = str(e)
            fk_error_mapping = {
                'Failed to validate role': ('role_id', RelationshipError, 'role'),
                'Failed to validate department': ('department_id', RelationshipError, 'department'),
                # Used hardcoded error messages from entity_validators as SQLAlchemy will not validate fks
                # due to polymorphic association on staff table
            }
            for error, (attr_name, error_class, entity) in fk_error_mapping.items():
                if error in error_message:
                    raise error_class(error=error_message, operation='update', entity=entity)

            raise RelationshipError(error=error_message, operation='update', entity='unknown_entity')




    def archive_staff(self, staff_id: UUID, reason: ArchiveReason) -> Staff:
            """Archive staff.
            Args:
                staff_id (UUID): ID of staff to archive
                reason (ArchiveReason): Reason for archiving
            Returns:
                Staff: Archived staff record
            """
            try:
                return self.repository.archive(staff_id, SYSTEM_USER_ID, reason)

            except EntityNotFoundError as e:
                raise StaffNotFoundError(identifier=staff_id, detail = str(e))


    def delete_staff(self, staff_id: UUID) -> None:
        """Permanently delete a staff.
        Args:
            staff_id (UUID): ID of staff to delete
        """
        try:
            self.repository.delete(staff_id)

        except EntityNotFoundError as e:
            raise StaffNotFoundError(identifier=staff_id, detail = str(e))


        except RelationshipError as e:
            # Note: Referenced FKs are SET NULL on deletion, so RelationshipError may not trigger here,
            # but it is being kept for unexpected constraint issues.
            error_message = str(e)
            raise RelationshipError(error=error_message, operation='delete', entity='unknown_entity')



    def get_all_archived_staff(self, filters) -> List[Staff]:
        """Get all archived staff with filtering.
        Returns:
            List[Staff]: List of archived staff records
        """
        fields = ['name', 'staff_type']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_staff(self, staff_id: UUID) -> Staff:
        """Get an archived staff by ID.
        Args:
            staff_id: ID of staff to retrieve
        Returns:
            Staff: Retrieved staff record
        """
        try:
            return self.repository.get_archive_by_id(staff_id)
        except EntityNotFoundError as e:
            raise StaffNotFoundError(identifier=staff_id, detail = str(e))

    def restore_staff(self, staff_id: UUID) -> Staff:
        """Restore an archived staff.
        Args:
            staff_id: ID of staff to restore
        Returns:
            Staff: Restored staff record
        """
        try:
            archived = self.get_archived_staff(staff_id)
            archived.last_modified_by = SYSTEM_USER_ID
            return self.repository.restore(staff_id)
        except EntityNotFoundError as e:
            raise StaffNotFoundError(identifier=staff_id, detail = str(e))


    def delete_archived_staff(self, staff_id: UUID) -> None:
        """Permanently delete an archived staff.
        Args:
            staff_id: ID of staff to delete
        """
        try:
            self.repository.delete_archive(staff_id)
        except EntityNotFoundError as e:
            raise StaffNotFoundError(identifier=staff_id, detail = str(e))

        except RelationshipError as e:
            # Note: Referenced FKs are SET NULL on deletion, so RelationshipError may not trigger here,
            # but it is being kept for unexpected constraint issues.
            error_message = str(e)
            raise RelationshipError(error=error_message, operation='delete', entity='unknown_entity')





