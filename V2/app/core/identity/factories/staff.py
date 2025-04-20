from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from V2.app.core.shared.services.email_service.onboarding import OnboardingService
from V2.app.core.auth.services.password_service import PasswordService
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.core.shared.database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.identity.validators.identity import IdentityValidator
from V2.app.core.shared.database.models import Staff, Educator, SupportStaff, AdminStaff
from ...shared.errors.maps.error_map import error_map
from ...shared.errors import ArchiveDependencyError, EntityNotFoundError, StaffTypeError
from ...shared.errors.decorators.resolve_unique_violation import resolve_unique_violation
from ...shared.errors.decorators.resolve_fk_violation import (
    resolve_fk_on_update, resolve_fk_on_create, resolve_fk_on_delete
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
        self.validator = IdentityValidator()
        self.password_service = PasswordService(session)
        self.onboarding_service = OnboardingService()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.onboarding_service = OnboardingService()
        self.domain = "Staff"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_unique_violation({
        "staff_phone_key": ("phone", lambda self, staff_data: staff_data.phone),
        "staff_email_address_key": ("email_address", lambda self, staff_data: staff_data.email_address),
    })
    @resolve_fk_on_create()
    def create_staff_record(self, staff_data) -> [Staff, str]:
        """Internal method that just builds + persists the record."""
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
        return self.repository.create(new_staff), password


    def create_staff(self, staff_data) -> Staff:
        staff, password = self.create_staff_record(staff_data)
        full_name = f"{staff.first_name} {staff.last_name}"
        self.onboarding_service.send_staff_onboarding_email(
            staff.email_address, full_name, password
        )
        return staff


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


    @resolve_fk_on_update()
    @resolve_unique_violation({
        "staff_phone_key": ("phone", lambda self, data: data.get('phone')),
        "staff_email_address_key": ("email_address", lambda self, data: data.get('email_address')),
    })

    def update_staff(self, staff_id: UUID, data: dict) -> Staff:
        existing = self.get_staff(staff_id)
        original=data.copy()
        try:
            validations = {
                "first_name": (self.validator.validate_name, "first_name"),
                "last_name": (self.validator.validate_name, "last_name"),
                "email_address": (self.validator.validate_staff_email, "email_address"),
                "phone": (self.validator.validate_phone, "phone"),
                "address": (self.validator.validate_address, "address"),
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in original:
                    validated_value = validator_func(original.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            existing.last_modified_by = SYSTEM_USER_ID #placeholder
            return self.repository.update(staff_id, existing)

        except EntityNotFoundError as e:
            self.raise_not_found(staff_id, e)


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
                self.raise_not_found(staff_id, e)

    @resolve_fk_on_delete()
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
            self.raise_not_found(staff_id, e)


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
            self.raise_not_found(staff_id, e)

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
            self.raise_not_found(staff_id, e)

    @resolve_fk_on_delete()
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
            self.raise_not_found(staff_id, e)