from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.models.enums import StaffType, UserRoleName
from app.core.shared.services.email_service.onboarding import OnboardingService
from app.core.auth.services.password_service import PasswordService
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.identity.services.validators import IdentityValidator
from app.core.identity.models.staff import Staff, Educator, SupportStaff, AdminStaff
from app.core.rbac.services.role_service import RBACService
from ...shared.exceptions.maps.error_map import error_map
from ...shared.exceptions import (
    ArchiveDependencyError,
    EntityNotFoundError,
    StaffTypeError,
    DeletionDependencyError,
)
from ...shared.exceptions.decorators.resolve_unique_violation import (
    resolve_unique_violation,
)
from ...shared.exceptions.decorators.resolve_fk_violation import (
    resolve_fk_on_update,
    resolve_fk_on_create,
    resolve_fk_on_delete,
)


class StaffFactory(BaseFactory):
    """Factory class for managing staff operations."""

    def __init__(self, session: Session, model=Staff, current_user=None):
        super().__init__(current_user)
        """Initialize factory with db session, model and current actor.
            Args:
            session: SQLAlchemy db session
            model: Model class, defaults to Staff
            current_user: The authenticated user performing the operation, if any.
        """

        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = IdentityValidator()
        self.password_service = PasswordService(session)
        self.onboarding_service = OnboardingService()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session, current_user)
        self.rbac_service = RBACService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Staff"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name,
        )

    @resolve_unique_violation(
        {
            "staff_phone_key": ("phone", lambda self, data: data.phone),
            "staff_email_address_key": (
                "email_address",
                lambda self, data: data.email_address,
            ),
        }
    )
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
                "email_address": self.validator.validate_staff_email(
                    data.email_address
                ),
                "address": self.validator.validate_address(data.address),
                "phone": self.validator.validate_phone(data.phone),
                "date_joined": self.validator.validate_date(data.date_joined),
                "created_by": self.actor_id,
                "last_modified_by": self.actor_id,
                "current_role_id": self.rbac_service.fetch_role_id(
                    UserRoleName.INACTIVE.value
                ),
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
                    input_value=data.staff_type,
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
                entity_model=self.entity_model,
                identifier=staff_id,
                error=str(e),
                display_name=self.display_name,
            )

    def get_all_staff(self, filters) -> List[Staff]:
        """Get all active staff with filtering.
        Returns:
            List[Staff]: List of active staffs
        """
        fields = ["name", "staff_type", "department_id", "role_id"]
        return self.repository.execute_query(fields, filters)

    @resolve_fk_on_update()
    @resolve_unique_violation(
        {
            "staff_phone_key": ("phone", lambda self, *a: a[-1].get("phone")),
            "staff_email_address_key": (
                "email_address",
                lambda self, *a: a[-1].get("email_address"),
            ),
        }
    )
    def update_staff(self, staff_id: UUID, data: dict) -> Staff:
        """Update a staff profile information.
        Args:
            staff_id (UUID): ID of staff to update
            data (dict): Dictionary containing fields to update
        Returns:
            Staff: Updated staff record
        """
        copied_data = data.copy()
        try:
            existing = self.get_staff(staff_id)
            validations = {
                "first_name": (self.validator.validate_name, "first_name"),
                "last_name": (self.validator.validate_name, "last_name"),
                "email_address": (self.validator.validate_staff_email, "email_address"),
                "phone": (self.validator.validate_phone, "phone"),
                "address": (self.validator.validate_address, "address"),
            }
            # leave original data untouched for error message extraction
            for field, (validator_func, model_attr) in validations.items():
                if field in copied_data:
                    validated_value = validator_func(copied_data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in copied_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(staff_id, existing, modified_by=self.actor_id)

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
            staff = self.get_staff(staff_id)
            if staff.staff_type == StaffType.Educator:
                model, display_name = Educator, "educator"
            else:
                model, display_name = Staff, "staff"

            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=model, target_id=staff_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.model,
                    identifier=staff_id,
                    display_name=display_name,
                    related_entities=", ".join(failed_dependencies),
                )
            return self.repository.archive(staff_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(staff_id, e)

    @resolve_fk_on_delete(display="Staff Member")
    def delete_staff(self, staff_id: UUID) -> None:
        """Permanently delete a staff member if there are no dependent entities.
        Args:
            staff_id (UUID): ID of staff to delete
        """
        try:
            staff = self.get_staff(staff_id)

            if staff.staff_type == StaffType.Educator:
                model, display_name = Educator, "educator"
            else:
                model, display_name = Staff, "staff"

            failed_dependencies = self.delete_service.check_active_dependencies_exists(
                entity_model=model, target_id=staff_id
            )
            if failed_dependencies:
                raise DeletionDependencyError(
                    entity_model=model,
                    identifier=staff_id,
                    display_name=display_name,
                    related_entities=", ".join(failed_dependencies),
                )

            return self.repository.delete(staff_id)

        except EntityNotFoundError as e:
            self.raise_not_found(staff_id, e)

    def get_all_archived_staff(self, filters) -> List[Staff]:
        """Get all archived staff with filtering.
        Returns:
            List[Staff]: List of archived staff records
        """
        fields = ["name", "staff_type", "department_id", "role_id"]
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

    @resolve_fk_on_delete(display="Staff Member")
    def delete_archived_staff(self, staff_id: UUID) -> None:
        """Permanently delete an archived staff member if there are no dependent entities.
        Args:
            staff_id: ID of staff to delete
        """
        try:
            staff = self.get_archived_staff(staff_id)

            if staff.staff_type == StaffType.Educator:
                model, display_name = Educator, "educator"
            else:
                model, display_name = Staff, "staff"

            failed_dependencies = self.delete_service.check_active_dependencies_exists(
                entity_model=model, target_id=staff_id
            )
            if failed_dependencies:
                raise DeletionDependencyError(
                    entity_model=model,
                    identifier=staff_id,
                    display_name=self.display_name,
                    related_entities=", ".join(failed_dependencies),
                )

            self.repository.delete_archive(staff_id)

        except EntityNotFoundError as e:
            self.raise_not_found(staff_id, e)
