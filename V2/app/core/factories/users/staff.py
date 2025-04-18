from typing import List
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

from ...services.email.onboarding import OnboardingService
from ...services.lifecycle_service.archive_service import ArchiveService
from ...services.lifecycle_service.delete_service import DeleteService
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....core.validators.users import UserValidator
from ....core.services.auth.password_service import PasswordService
from ....database.models.users import Staff, Educator, SupportStaff, AdminStaff
from ...errors.fk_resolver import FKResolver

from ....core.errors.maps.error_map import error_map
from ....core.errors.maps.fk_mapper import fk_error_map
from ...errors import (
    DuplicateEntityError, ArchiveDependencyError, EntityNotFoundError, UniqueViolationError,
    RelationshipError,StaffTypeError
)


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class StaffFactory:
    """Factory class for managing staff operations."""

    def __init__(self, session: Session, model = Staff):
        """Initialize factory with model and database session.
            Args:
            session: SQLAlchemy database session
            model: Model class, defaults to Staff
        """

        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = UserValidator()
        self.password_service = PasswordService(session)
        self.onboarding_service = OnboardingService()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.onboarding_service = OnboardingService()
        self.domain = "Staff"


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

        except UniqueViolationError as e:
            error_message = str(e).lower()
            unique_violation_map = {
                "staff_phone_key": ("phone", staff_data.phone),
                "staff_email_address_key": ("email_address", staff_data.email_address),
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
                factory_class=self.__class__, error_message=str(e), context_obj=new_staff,
                operation="create", fk_map=fk_error_map
            )
            if resolved:
                raise resolved

            raise RelationshipError(
                error=str(e), operation="create", entity_model="unknown", domain=self.domain
            )


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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=staff_id, error=str(e),
                display_name=self.display_name
            )


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
            unique_violation_map = {
                "staff_phone_key": ("phone", original.get('phone', 'unknown')),
                "staff_email_address_key": ("email_address", original.get('email_address', 'unknown')),
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


    def archive_staff(self, staff_id: UUID, reason) -> Staff:
            """Archive staff members if no active dependencies exist.
            Args:
                staff_id (UUID): ID of staff to archive
                reason: Reason for archiving
            Returns:
                Staff: Archived staff record
            """
            try:
                failed_dependencies = self.archive_service.check_active_dependencies_exists(
                    entity_model=self.model,
                    target_id=staff_id
                )
                if failed_dependencies:
                    raise ArchiveDependencyError(
                        entity_model=self.entity_model, identifier=staff_id,
                        display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                    )
                return self.repository.archive(staff_id, SYSTEM_USER_ID, reason)

            except EntityNotFoundError as e:
                raise EntityNotFoundError(
                    entity_model=self.entity_model, identifier=staff_id, error=str(e),
                    display_name=self.display_name
                )


    def delete_staff(self, staff_id: UUID, is_archived = False) -> None:
        """Permanently delete a staff member if there are no dependent entities.
        Args:
            staff_id (UUID): ID of staff to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, staff_id, is_archived)
            return self.repository.delete(staff_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=staff_id, error=str(e),
                display_name=self.display_name
            )
        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model=self.model.__name__, domain=self.domain
            )


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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=staff_id, error=str(e),
                display_name=self.display_name
            )


    def restore_staff(self, staff_id: UUID) -> Staff:
        """Restore an archived staff.
        Args:
            staff_id: ID of staff to restore
        Returns:
            Staff: Restored staff record
        """
        try:
            return self.repository.restore(staff_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=staff_id, error=str(e),
                display_name=self.display_name
            )


    def delete_archived_staff(self, staff_id: UUID, is_archived = True) -> None:
        """Permanently delete an archived staff member if there are no dependent entities.
        Args:
            staff_id: ID of staff to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, staff_id, is_archived)
            self.repository.delete_archive(staff_id)

        except EntityNotFoundError as e:
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=staff_id, error=str(e),
                display_name=self.display_name
            )

        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model=self.model.__name__, domain=self.domain
            )



