import random
import string
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.shared.exceptions import CurrentPasswordError
from app.core.shared.exceptions import PasswordFormatError
from app.core.shared.services.email_service.password import PasswordEmailService
from app.core.shared.exceptions.auth_errors import (
    WrongPasswordError,
    InvalidCredentialsError,
    ResetLinkExpiredError,
    InvalidPasswordTokenError,
)
from app.core.auth.services.token_service import TokenService
from app.infra.db.redis_db.access_tokens import token_blocklist
from app.infra.db.redis_db.password_tokens import password_token_list
from app.core.identity.models.guardian import Guardian
from app.core.identity.models.staff import Staff
from app.core.identity.models.student import Student
from app.core.shared.schemas.enums import UserType
from app.core.shared.log_service.logger import auth_logger
from app.settings import config

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    """
    Service for managing password operations across all user types.

    Handles password hashing, generation, changes, and reset flows. Supports different reset workflows per user type:
    - Students/Guardians: "forgot password" generates a new random password
      and emails it to the guardian.
    - Staff: "forgot password" sends a time-limited reset link via email.

    Integrates with Redis for token management (blocklisting access tokens
    after password change, storing temporary password reset tokens).

    Attributes:
        session: SQLAlchemy database session.
        blocklist: Redis-backed access token blocklist for revocation.
        token_list: Redis-backed storage for password reset tokens.
        validator: AuthValidator instance for password validation rules.
        email_service: PasswordEmailService for sending notifications.
        token_service: TokenService instance for JWT operations.
    """

    def __init__(self, session: Session):
        """
        Initialize the PasswordService with a database session.

        Args:
            session: An active SQLAlchemy Session instance for database operations.
        """
        self.session = session
        self.blocklist = token_blocklist
        self.token_list = password_token_list
        self.email_service = PasswordEmailService()
        self.token_service = TokenService()

    @staticmethod
    def validate_password(password: str):
        """
        Validate a password against security requirements.

        Requirements:
            - Not empty
            - Length between 8 and 12 characters (inclusive)
            - At least one uppercase letter
            - At least one lowercase letter
            - At least one digit
            - At least one special character (non-alphanumeric)

        Args:
            password: The plaintext password to validate.

        Returns:
            str: The validated password (unchanged) if all requirements are met.

        Raises:
            PasswordFormatError: If any validation requirement fails. Note that
                the error does not specify which requirement(s) failed.
        """
        is_valid = True

        if not password:
            is_valid = False

        if len(password) < 8 or len(password) > 12:
            is_valid = False

        if not any(char.isupper() for char in password):
            is_valid = False

        if not any(char.islower() for char in password):
            is_valid = False

        if not any(char.isdigit() for char in password):
            is_valid = False

        if not any(not char.isalnum() for char in password):
            is_valid = False

        if not is_valid:
            raise PasswordFormatError()

        return password


    @staticmethod
    def generate_random_password():
        """
        Creates a password from ASCII letters and special characters (!@#$%&),shuffled for randomness.
        Returns:
            str: A randomly generated 10-character password.
        """
        length = 10
        characters = list(string.ascii_letters + "!@#$%&")
        random.shuffle(characters)
        password = []
        for item in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        password = "".join(password)
        return password

    @staticmethod
    def hash_password(password: str):
        """
        Hash a plaintext password using bcrypt.
        Args:
            password: The plaintext password to hash.
        Returns:
            str: The bcrypt-hashed password string.
        """
        hashed_password = bcrypt_context.hash(password)
        return hashed_password

    def change_password(
        self, user, current_password: str, new_password: str, token_data: dict
    ):
        """
        Change a user's password and send appropriate notifications.

        Validates the current password, ensures the new password differs from
        the current one, hashes and saves the new password, then sends email
        notifications based on user type:
        - Students: notifies the guardian of the password change.
        - Guardians/Staff: notifies the user directly.

        After successful change, revokes the current access token to force
        re-authentication.

        Args:
            user: The user model instance (Student, Guardian, or Staff).
            current_password: The user's current plaintext password for verification.
            new_password: The desired new plaintext password.
            token_data: Dict containing the current JWT token data, used for
                extracting identity info and revoking the token.

        Returns:
            bool: True if password change and token revocation succeeded.

        Raises:
            WrongPasswordError: If current_password doesn't match the stored hash.
            CurrentPasswordError: If new_password matches the current password.
            ValidationError: If new_password fails validation rules (propagated
                from AuthValidator).

        Note:
            Token revocation failures are logged but do not raise exceptions;
            the password change itself still succeeds.
        """

        identity = token_data["identity"]
        user_id = identity.get("user_id", user.id)

        user_type = identity["user_type", user.user_type]

        if not bcrypt_context.verify(current_password, user.password_hash):
            raise WrongPasswordError(user_id=user_id)
        if bcrypt_context.verify(new_password, user.password_hash):
            raise CurrentPasswordError(user_id=user_id)

        new_password = self.validate_password(new_password)
        user.password_hash = self.hash_password(new_password)
        self.session.commit()

        # send notification based on user type

        if user_type == UserType.STUDENT:
            # find the student's guardian to notify them via email
            student_guardian = (
                self.session.execute(
                    select(Guardian).where(Guardian.id == user.guardian_id)
                )
                .scalars()
                .one_or_none()
            )

            guardian_name = (
                f"{student_guardian.title.value} {student_guardian.last_name}"
            )
            guardian_email = student_guardian.email_address
            student_name = f"{user.first_name} {user.last_name}"
            self.email_service.send_ward_password_change_alert(
                guardian_email, guardian_name, student_name
            )

        elif user_type == UserType.GUARDIAN:
            email = user.email_address
            name = f"{user.title.value} {user.last_name}"

            self.email_service.send_password_change_notification(email, name)

        elif user_type == UserType.STAFF:
            email = user.email_address
            name = f"{user.first_name}"

            self.email_service.send_password_change_notification(email, name)

        try:
            self.blocklist.revoke_token(token_data)
            return True
        except Exception as redis_error:
            auth_logger.error(
                f"Password was reset but token revocation failed for user {user_id}: {redis_error}"
            )

    def forgot_password(self, identifier: str, user_type: UserType):
        """
        Generate and email a new random password for students or guardians.

        Generates a random password, updates the user's password hash, and
        emails the new password:
        - Guardians: email sent directly to the guardian.
        - Students: email sent to the student's guardian with the student's name.

        Args:
            identifier: The user's identifier (email for guardians, student_id
                for students).
            user_type: UserType enum (STUDENT or GUARDIAN). Staff should use
                request_password_reset() instead.

        Raises:
            InvalidCredentialsError: If no user is found with the given identifier.

        Note:
            Staff members are not supported by this method; they must use the
            reset link flow via request_password_reset().
        """
        password = self.generate_random_password()

        if user_type == UserType.GUARDIAN:
            stmt = select(Guardian).where(Guardian.email_address == identifier)
            guardian = self.session.execute(stmt).scalar_one_or_none()

            if not guardian:
                raise InvalidCredentialsError(credential=identifier)

            guardian.password_hash = self.hash_password(password)

            full_name = f"{guardian.title}. {guardian.last_name}"
            self.email_service.send_guardian_new_password(
                guardian.email_address, full_name, password
            )

            self.session.commit()

        elif user_type == UserType.STUDENT:
            stmt = select(Student).where(Student.student_id == identifier)
            student = self.session.execute(stmt).scalar_one_or_none()

            if not student:
                raise InvalidCredentialsError(credential=identifier)

            guardian = self.session.execute(
                select(Guardian).where(Guardian.id == student.guardian_id)
            ).scalar_one_or_none()

            student.password_hash = self.hash_password(password)

            full_name = f"{guardian.title.value}. {guardian.last_name}"

            self.email_service.send_ward_new_password(
                guardian.email_address,
                full_name,
                password,
                student.first_name,
                student.last_name,
            )

            self.session.commit()

    def request_password_reset(self, email_address: str):
        """
        Initiate password reset flow for staff by sending a reset link.

        Verifies the email belongs to a staff member, generates a time-limited
        reset token stored in Redis, and emails a reset URL to the user.

        Args:
            email_address: The staff member's email address.

        Raises:
            InvalidCredentialsError: If no staff member exists with the given email.

        Note:
            This method is staff-only. Students and guardians use
            forgot_password() which generates a new password directly.
        """
        # only staff are required to request a reset link after forgetting

        # authenticate a staff email without validating a password
        stmt = select(Staff).where(Staff.email_address == email_address.lower())
        user = self.session.execute(stmt).scalars().first()

        if not user:
            raise InvalidCredentialsError(credential=email_address)

        token = self.token_list.save_password_token(email_address)

        reset_url = F"{config.RESET_URL}{token}"      f"https://kademia.com/staff/reset-password?token={token}"

        self.email_service.send_staff_reset_link(
            user.email_address, user.first_name, reset_url
        )

    def reset_password(self, password_token: str, new_password: str):
        """
        Complete password reset using a token from a reset link.

        Validates the reset token, retrieves the associated email, updates the
        staff member's password, and deletes the used token from Redis.

        Args:
            password_token: The token from the password reset URL.
            new_password: The desired new plaintext password.

        Raises:
            ResetLinkExpiredError: If the token has expired or been used.
            InvalidPasswordTokenError: If the token exists but has no associated email.
            InvalidCredentialsError: If no staff member exists for the token's email.
            ValidationError: If new_password fails validation rules.

        Note:
            Token deletion failures are logged but do not raise exceptions;
            the password reset itself still succeeds.
        """

        if not self.token_list.is_token_active(password_token):
            raise ResetLinkExpiredError(token=password_token)

        email_address = self.token_list.get_email_from_token(password_token)
        if not email_address:
            raise InvalidPasswordTokenError(token=password_token)

        stmt = select(Staff).where(Staff.email_address == email_address.lower())
        user = self.session.execute(stmt).scalars().first()

        if not user:
            raise InvalidCredentialsError(credential=email_address)

        new_password = self.validate_password(new_password)
        user.password_hash = self.hash_password(new_password)
        self.session.commit()

        try:
            self.token_list.redis.delete(f"{self.token_list.key_pref}{password_token}")
        except Exception as redis_error:
            auth_logger.error(
                f"Password was reset but password token revocation failed for user {user.id}: {redis_error}"
            )
