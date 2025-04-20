from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from ...services.email.onboarding import OnboardingService
from ...services.auth.password_service import PasswordService
from ...services.lifecycle_service.archive_service import ArchiveService
from ...services.lifecycle_service.delete_service import DeleteService
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....core.validators.users import UserValidator
from ....database.models.users import Guardian

from ....core.errors.maps.error_map import error_map
from ...errors import ArchiveDependencyError, EntityNotFoundError
from ...errors.decorators.resolve_unique_violation import resolve_unique_violation
from ...errors.decorators.resolve_fk_violation import (
    resolve_fk_on_update, resolve_fk_on_create, resolve_fk_on_delete
)

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class GuardianFactory:
    """Factory class for managing guardian operations."""

    def __init__(self, session: Session, model = Guardian):
        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = UserValidator()
        self.password_service = PasswordService(session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.onboarding_service = OnboardingService()
        self.domain = "Guardian"


    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )

    @resolve_unique_violation({
        "guardians_phone_key": ("phone", lambda self, guardian_data: guardian_data.phone),
        "guardians_email_address_key": ("email_address", lambda self, guardian_data: guardian_data.email_address),
    })
    @resolve_fk_on_create()
    def create_guardian_record(self, guardian_data) -> [Guardian, str]:
        password = self.password_service.generate_random_password()
        new_guardian = Guardian(
            id=uuid4(),
            title=guardian_data.title,
            first_name=self.validator.validate_name(guardian_data.first_name),
            last_name=self.validator.validate_name(guardian_data.last_name),
            password_hash=self.password_service.hash_password(password),
            gender=guardian_data.gender,
            email_address=self.validator.validate_email_address(guardian_data.email_address),
            address=self.validator.validate_address(guardian_data.address),
            phone=self.validator.validate_phone(guardian_data.phone),
            created_by=SYSTEM_USER_ID,
            last_modified_by=SYSTEM_USER_ID,
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
        try:
            return self.repository.get_by_id(guardian_id)

        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)


    def get_all_guardians(self, filters) -> List[Guardian]:
        fields = ['name']
        return self.repository.execute_query(fields, filters)


    @resolve_fk_on_update()
    @resolve_unique_violation({
        "guardians_phone_key": ("phone", lambda self, data: data.get('phone')),
        "guardians_email_address_key": ("email_address", lambda self, data: data.get('email_address')),
    })
    def update_guardian(self, guardian_id: UUID, data: dict) -> Guardian:
        original = data.copy()
        existing = self.get_guardian(guardian_id)
        try:
            validations = {
                "first_name": (self.validator.validate_name, "first_name"),
                "last_name": (self.validator.validate_name, "last_name"),
                "email_address": (self.validator.validate_email_address, "email_address"),
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

            existing.last_modified_by = SYSTEM_USER_ID
            return self.repository.update(guardian_id, existing)

        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)


    def archive_guardian(self, guardian_id: UUID, reason) -> Guardian:
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
            return self.repository.archive(guardian_id, SYSTEM_USER_ID, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)


    @resolve_fk_on_delete()
    def delete_guardian(self, guardian_id: UUID, is_archived = False) -> None:
        try:
            self.delete_service.check_safe_delete(self.model, guardian_id, is_archived)
            return self.repository.delete(guardian_id)

        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)


    def get_all_archived_guardians(self, filters) -> List[Guardian]:
        fields = ['name']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_guardian(self, guardian_id: UUID) -> Guardian:
        try:
            return self.repository.get_archive_by_id(guardian_id)
        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)


    def restore_guardian(self, guardian_id: UUID) -> Guardian:
        try:
            return self.repository.restore(guardian_id)
        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)


    @resolve_fk_on_delete()
    def delete_archived_guardian(self, guardian_id: UUID, is_archived = True) -> None:
        try:
            self.delete_service.check_safe_delete(self.model, guardian_id, is_archived)
            self.repository.delete_archive(guardian_id)

        except EntityNotFoundError as e:
            self.raise_not_found(guardian_id, e)
