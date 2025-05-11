from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from V2.app.core.shared.factory.base_factory import BaseFactory
from V2.app.core.shared.services.email_service.onboarding import OnboardingService
from V2.app.core.auth.services.password_service import PasswordService
from V2.app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from V2.app.core.shared.services.lifecycle_service.delete_service import DeleteService
from V2.app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from V2.app.core.identity.validators import IdentityValidator
from V2.app.core.identity.models.guardian import Guardian
from V2.app.core.shared.exceptions.maps.error_map import error_map
from V2.app.core.shared.exceptions import ArchiveDependencyError, EntityNotFoundError
from V2.app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from V2.app.core.shared.exceptions.decorators.resolve_fk_violation import (
    resolve_fk_on_update, resolve_fk_on_create, resolve_fk_on_delete
)



class GuardianFactory(BaseFactory):
    """Factory class for managing guardian operations."""

    def __init__(self, session: Session, model = Guardian, current_user = None):#
        super().__init__(current_user)
        """Initialize factory with db session, model and current actor.
            Args:
            session: SQLAlchemy db session
            model: Model class, defaults to Guardian
            current_user: The authenticated user performing the operation, if any.
        """

        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = IdentityValidator()
        self.password_service = PasswordService(session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.onboarding_service = OnboardingService()
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Guardian"


    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_unique_violation({
        "guardians_phone_key": ("phone", lambda self, data: data.phone),
        "guardians_email_address_key": ("email_address", lambda self, data: data.email_address),
    })
    @resolve_fk_on_create()
    def create_guardian_record(self, data) ->  [Guardian, str]:
        """Create a new guardian.
        Args:
            data: guardian data
        Returns:
            guardian: Created guardian record
            password: guardian's password
        """
        password = self.password_service.generate_random_password()
        new_guardian = Guardian(
            id=uuid4(),
            title=data.title,
            first_name=self.validator.validate_name(data.first_name),
            last_name=self.validator.validate_name(data.last_name),
            password_hash=self.password_service.hash_password(password),
            gender=data.gender,
            email_address=self.validator.validate_email_address(data.email_address),
            address=self.validator.validate_address(data.address),
            phone=self.validator.validate_phone(data.phone),
            created_by=self.actor_id,
            last_modified_by=self.actor_id,
        )
        return self.repository.create(new_guardian), password


    def create_guardian(self, guardian_data) -> Guardian:
        guardian, password = self.create_guardian_record(guardian_data)
        full_name = f"{guardian.title.value}. {guardian.last_name}"
        self.onboarding_service.send_guardian_onboarding_email(
            guardian.email_address, full_name, password
        )
        return guardian


    def get_guardian(self, guardian_id: UUID) -> Guardian:
        """Get a specific guardian by id.
        Args:
            guardian_id (UUID): id of guardian to retrieve
        Returns:
            guardian: Retrieved guardian record
        """
        try:
            return self.repository.get_by_id(guardian_id)

        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)


    def get_all_guardians(self, filters) -> List[Guardian]:
        """Get all active guardian with filtering.
        Returns:
            List[guardian]: List of active guardians
        """
        fields = ['name']
        return self.repository.execute_query(fields, filters)



    @resolve_fk_on_update()
    @resolve_unique_violation({
        "guardians_phone_key": ("phone", lambda self, *a: a[-1].get("phone")),
        "guardians_email_address_key": ("email_address", lambda self, *a: a[-1].get("email_address")),
    })
    def update_guardian(self, guardian_id: UUID, data: dict) -> Guardian:
        """Update a guardian profile information.
        Args:
            guardian_id (UUID): ID of guardian to update
            data (dict): Dictionary containing fields to update
        Returns:
            guardian: Updated guardian record
        """
        copied_data = data.copy()
        existing = self.get_guardian(guardian_id)
        try:
            validations = {
                "first_name": (self.validator.validate_name, "first_name"),
                "last_name": (self.validator.validate_name, "last_name"),
                "email_address": (self.validator.validate_email_address, "email_address"),
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

            return self.repository.update(guardian_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)


    def archive_guardian(self, guardian_id: UUID, reason) -> Guardian:
        """Archive guardian if no active dependencies exist.
        Args:
            guardian_id (UUID): ID of guardian to archive
            reason: Reason for archiving
        Returns:
            guardian: Archived guardian record
        """
        try:
            failed_dependencies = self.archive_service.check_active_dependencies_exists(
                entity_model=self.model,
                target_id=guardian_id
            )
            if failed_dependencies:
                raise ArchiveDependencyError(
                    entity_model=self.entity_model, identifier=guardian_id,
                    display_name=self.display_name, related_entities=", ".join(failed_dependencies)
                )
            return self.repository.archive(guardian_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)


    @resolve_fk_on_delete()
    def delete_guardian(self, guardian_id: UUID, is_archived = False) -> None:
        """Permanently delete an active guardian if there are no dependent entities.
        Args:
            guardian_id (UUID): ID of guardian to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, guardian_id, is_archived)
            return self.repository.delete(guardian_id)

        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)


    def get_all_archived_guardians(self, filters) -> List[Guardian]:
        """Get all archived guardian with filtering.
        Returns:
            List[guardian]: List of archived guardian records
        """
        fields = ['name']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_guardian(self, guardian_id: UUID) -> Guardian:
        """Get an archived guardian by ID.
        Args:
            guardian_id: ID of guardian to retrieve
        Returns:
            guardian: Retrieved guardian record
        """
        try:
            return self.repository.get_archive_by_id(guardian_id)
        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)


    def restore_guardian(self, guardian_id: UUID) -> Guardian:
        """Restore an archived guardian.
        Args:
            guardian_id: ID of guardian to restore
        Returns:
            guardian: Restored guardian record
        """
        try:
            return self.repository.restore(guardian_id)
        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)


    @resolve_fk_on_delete()
    def delete_archived_guardian(self, guardian_id: UUID, is_archived = True) -> None:
        """Permanently delete an archived guardian if there are no dependent entities.
        Args:
            guardian_id: ID of guardian to delete
            is_archived: Whether to check archived or active entities
        """
        try:
            self.delete_service.check_safe_delete(self.model, guardian_id, is_archived)
            self.repository.delete_archive(guardian_id)

        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)