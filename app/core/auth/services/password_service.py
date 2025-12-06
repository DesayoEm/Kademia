import random
import string
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.shared.exceptions import CurrentPasswordError
from app.core.shared.services.email_service.password import PasswordEmailService
from app.core.shared.exceptions.auth_errors import (
    WrongPasswordError,
    InvalidCredentialsError,
    ResetLinkExpiredError,
    InvalidPasswordTokenError,
)
from app.core.auth.validators.auth import AuthValidator
from app.core.auth.services.token_service import TokenService
from app.infra.db.redis_db.access_tokens import token_blocklist
from app.infra.db.redis_db.password_tokens import password_token_list
from app.core.identity.models.guardian import Guardian
from app.core.identity.models.staff import Staff
from app.core.identity.models.student import Student
from app.core.shared.schemas.enums import UserType
from app.core.shared.log_service.logger import auth_logger

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:

    def __init__(self, session: Session):
        self.session = session
        self.blocklist = token_blocklist
        self.token_list = password_token_list
        self.validator = AuthValidator()
        self.email_service = PasswordEmailService()
        self.token_service = TokenService()

    @staticmethod
    def generate_random_password():
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
        hashed_password = bcrypt_context.hash(password)
        return hashed_password

    def change_password(
        self, user, current_password: str, new_password: str, token_data: dict
    ):
        identity = token_data["identity"]
        user_id = identity.get("user_id", user.id)

        user_type = identity["user_type", user.user_type]

        if not bcrypt_context.verify(current_password, user.password_hash):
            raise WrongPasswordError(user_id=user_id)
        if bcrypt_context.verify(new_password, user.password_hash):
            raise CurrentPasswordError(user_id=user_id)

        new_password = self.validator.validate_password(new_password)
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
        # only staff are required to request a reset link after forgetting

        # authenticate a staff email without validating a password
        stmt = select(Staff).where(Staff.email_address == email_address.lower())
        user = self.session.execute(stmt).scalars().first()

        if not user:
            raise InvalidCredentialsError(credential=email_address)

        token = self.token_list.save_password_token(email_address)

        reset_url = f"https://kademia.com/staff/reset-password?token={token}"

        self.email_service.send_staff_reset_link(
            user.email_address, user.first_name, reset_url
        )

    def reset_password(self, password_token: str, new_password: str):

        if not self.token_list.is_token_active(password_token):
            raise ResetLinkExpiredError(token=password_token)

        email_address = self.token_list.get_email_from_token(password_token)
        if not email_address:
            raise InvalidPasswordTokenError(token=password_token)

        stmt = select(Staff).where(Staff.email_address == email_address.lower())
        user = self.session.execute(stmt).scalars().first()

        if not user:
            raise InvalidCredentialsError(credential=email_address)

        new_password = self.validator.validate_password(new_password)
        user.password_hash = self.hash_password(new_password)
        self.session.commit()

        try:
            self.token_list.redis.delete(f"{self.token_list.key_pref}{password_token}")
        except Exception as redis_error:
            auth_logger.error(
                f"Password was reset but password token revocation failed for user {user.id}: {redis_error}"
            )
