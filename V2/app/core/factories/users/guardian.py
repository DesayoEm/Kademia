from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session

from ...services.auth.email_service import EmailService
from ....core.errors.database_errors import RelationshipError, UniqueViolationError,EntityNotFoundError
from ...errors.user_errors import DuplicateGuardianError,GuardianNotFoundError
from ...services.auth.password_service import PasswordService
from ....database.db_repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from ....database.models.enums import ArchiveReason
from ....core.validators.users import UserValidator
from ....database.models.users import Guardian

SYSTEM_USER_ID = UUID('00000000-0000-0000-0000-000000000000')


class GuardianFactory:
    """Factory class for managing guardian operations."""

    def __init__(self, session: Session):
        self.repository = SQLAlchemyRepository(Guardian, session)
        self.validator = UserValidator()
        self.password_service = PasswordService(session)
        self.email_service = EmailService()
        

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
        try:
            self.email_service.send_guardian_onboarding_email(
                new_guardian.email_address, new_guardian.title, new_guardian.last_name, password
            )

            return self.repository.create(new_guardian)
        except UniqueViolationError as e:
            error_message = str(e).lower()
            if "guardians_phone_key" in error_message:
                raise DuplicateGuardianError(
                    input_value=guardian_data.phone, detail=error_message, field = "phone")
            elif "guardians_email_address_key" in error_message:
                raise DuplicateGuardianError(
                    input_value=guardian_data.email_address, detail=error_message,
                    field="email_address")
            else:
                raise DuplicateGuardianError(
                    input_value="unknown field",detail=error_message,
                         field = "Unknown")
        except RelationshipError as e:
            raise RelationshipError(error=str(e), operation='create', entity='unknown_entity')


    def get_guardian(self, guardian_id: UUID) -> Guardian:
        """Get a specific guardian by ID.
        Args:
            guardian_id (UUID): ID of guardian to retrieve
        Returns:
            guardian: Retrieved guardian record
        """
        try:
            return self.repository.get_by_id(guardian_id)
        except EntityNotFoundError as e:
            raise GuardianNotFoundError(id=guardian_id, detail = str(e))


    def get_all_guardians(self, filters) -> List[Guardian]:
        """Get all active guardian with filtering.
        Returns:
            List[guardian]: List of active guardians
        """
        fields = ['first_name','last_name', 'guardian_id']
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

            if 'first_name' in data:
                existing.first_name = self.validator.validate_name(data.pop('first_name'))
            if 'last_name' in data:
                existing.last_name = self.validator.validate_name(data.pop('last_name'))
            if 'email_address' in data:
                existing.email_address = self.validator.validate_email_address(data.pop('email_address'))
            if 'address' in data:
                existing.address = self.validator.validate_address(data.pop('address'))
            if 'phone' in data:
                existing.phone = self.validator.validate_phone(data.pop('phone'))


            for key, value in data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            existing.last_modified_by = SYSTEM_USER_ID
            return self.repository.update(guardian_id, existing)

        except UniqueViolationError as e:
            error_message = str(e).lower()
            if "guardians_phone_key" in error_message:
                raise DuplicateGuardianError(
                    input_value=original.get('phone', 'unknown'), detail=error_message,
                    field = "phone")
            elif "guardians_email_address_key" in error_message:
                raise DuplicateGuardianError(
                    input_value=original.get('email_address', 'unknown'), detail=error_message,
                    field = "email_address")
            else:
                raise DuplicateGuardianError(
                    input_value="unknown field",detail=error_message, field ="unknown")

        except RelationshipError as e:
            raise RelationshipError(error=str(e), operation='update', entity='unknown')


    def archive_guardian(self, guardian_id: UUID, reason: ArchiveReason) -> Guardian:
            """Archive guardian.
            Args:
                guardian_id (UUID): ID of guardian to archive
                reason (ArchiveReason): Reason for archiving
            Returns:
                guardian: Archived guardian record
            """
            try:
                return self.repository.archive(guardian_id, SYSTEM_USER_ID, reason)
            except EntityNotFoundError as e:
                raise GuardianNotFoundError(id=guardian_id, detail = str(e))


    def delete_guardian(self, guardian_id: UUID) -> None:
        """Permanently delete a guardian.
        Args:
            guardian_id (UUID): ID of guardian to delete
        """
        try:
            self.repository.delete(guardian_id)
        except EntityNotFoundError as e:
            raise GuardianNotFoundError(id=guardian_id, detail = str(e))


    def get_all_archived_guardians(self, filters) -> List[Guardian]:
        """Get all archived guardian with filtering.
        Returns:
            List[guardian]: List of archived guardian records
        """
        fields = ['first_name','last_name', 'guardian_id']
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
            raise GuardianNotFoundError(id=guardian_id, detail = str(e))

    def restore_guardian(self, guardian_id: UUID) -> Guardian:
        """Restore an archived guardian.
        Args:
            guardian_id: ID of guardian to restore
        Returns:
            guardian: Restored guardian record
        """
        try:
            archived = self.get_archived_guardian(guardian_id)
            archived.last_modified_by = SYSTEM_USER_ID
            return self.repository.restore(guardian_id)
        except EntityNotFoundError as e:
            raise GuardianNotFoundError(id=guardian_id, detail = str(e))


    def delete_archived_guardian(self, guardian_id: UUID) -> None:
        """Permanently delete an archived guardian.
        Args:
            guardian_id: ID of guardian to delete
        """
        try:
            self.repository.delete_archive(guardian_id)
        except EntityNotFoundError as e:
            raise GuardianNotFoundError(id=guardian_id, detail = str(e))




