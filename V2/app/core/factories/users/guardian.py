from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from ...errors.fk_resolver import FKResolver
from ...services.email.onboarding import OnboardingService
from ...services.auth.password_service import PasswordService
from ...services.lifecycle_service.archive_service import ArchiveService
from ...services.lifecycle_service.delete_service import DeleteService
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....core.validators.users import UserValidator
from ....database.models.users import Guardian

from ....core.errors.maps.error_map import error_map
from ....core.errors.maps.fk_mapper import fk_error_map
from ...errors import (
    DuplicateEntityError, ArchiveDependencyError, EntityNotFoundError, UniqueViolationError, RelationshipError
)


SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class GuardianFactory:
    """Factory class for managing guardian operations."""

    def __init__(self, session: Session, model = Guardian):
        """Initialize factory with model and database session.
            Args:
            session: SQLAlchemy database session
            model: Model class, defaults to Guardian
        """

        self.model = model
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = UserValidator()
        self.password_service = PasswordService(session)
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.onboarding_service= OnboardingService()
        self.domain = "Guardian"
        

    def create_guardian(self, guardian_data) -> Guardian:
        """Create a new guardian.
        Args:
            guardian_data: guardian data
        Returns:
            guardian: Created guardian record
        """
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
        full_name = f"{new_guardian.title.value}. {new_guardian.last_name}"
        try:
            self.onboarding_service.send_guardian_onboarding_email(
                new_guardian.email_address, full_name, password
            )
            return self.repository.create(new_guardian)

        except UniqueViolationError as e:
            error_message = str(e).lower()
            unique_violation_map = {
                "guardians_phone_key": ("phone", new_guardian.phone),
                "guardians_email_address_key": ("email_address", new_guardian.email_address),
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
                factory_class=self.__class__, error_message=str(e), context_obj=new_guardian,
                operation="create", fk_map=fk_error_map
            )
            if resolved:
                raise resolved
            raise RelationshipError(
                error=str(e), operation="create", entity_model="unknown", domain=self.domain
            )


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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=guardian_id, error=str(e),
                display_name=self.display_name
            )


    def get_all_guardians(self, filters) -> List[Guardian]:
        """Get all active guardian with filtering.
        Returns:
            List[guardian]: List of active guardians
        """
        fields = ['name']
        return self.repository.execute_query(fields, filters)


    def update_guardian(self, guardian_id: UUID, data: dict) -> Guardian:
        """Update a guardian profile information.
        Args:
            guardian_id (UUID): ID of guardian to update
            data (dict): Dictionary containing fields to update
        Returns:
            guardian: Updated guardian record
        """
        original = data.copy()
        try:
            existing = self.get_guardian(guardian_id)

            validations = {
                "first_name": (self.validator.validate_name, "first_name"),
                "last_name": (self.validator.validate_name, "last_name"),
                "email_address": (self.validator.validate_email_address, "email_address"),
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
            return self.repository.update(guardian_id, existing)

        except UniqueViolationError as e:
            error_message = str(e).lower()
            unique_violation_map = {
                "guardians_phone_key": ("phone", original.get('phone', 'unknown')),
                "guardians_email_address_key": ("email_address", original.get('email_address', 'unknown')),
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
                return self.repository.archive(guardian_id, SYSTEM_USER_ID, reason)

            except EntityNotFoundError as e:
                raise EntityNotFoundError(
                    entity_model=self.entity_model, identifier=guardian_id, error=str(e),
                    display_name=self.display_name
                )


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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=guardian_id, error=str(e),
                display_name=self.display_name
            )
        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model=self.model.__name__, domain=self.domain
            )


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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=guardian_id, error=str(e),
                display_name=self.display_name
            )


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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=guardian_id, error=str(e),
                display_name=self.display_name
            )


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
            raise EntityNotFoundError(
                entity_model=self.entity_model, identifier=guardian_id, error=str(e),
                display_name=self.display_name
            )

        except RelationshipError as e:
            raise RelationshipError(
                error=str(e), operation='delete', entity_model=self.model.__name__, domain=self.domain
            )




