import random
import string

import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import select

from V2.app.core.shared.services.email_service.password_reset import PasswordEmailService
from V2.app.core.shared.exceptions.auth_errors import WrongPasswordError, InvalidCredentialsError, ResetLinkExpiredError
from V2.app.core.auth.validators.auth import AuthValidator
from V2.app.core.auth.services.token_service import TokenService
from V2.app.infra.db.redis.access_tokens import token_blocklist
from V2.app.infra.db.redis.password_tokens import password_token_list
from V2.app.core.identity.models.guardian import Guardian
from V2.app.core.identity.models.staff import Staff
from V2.app.core.identity.models.student import Student
from V2.app.core.shared.schemas.enums import UserType
from V2.app.infra.log_service.logger import logger, auth_logger

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

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


    def change_password(self, user, current_password: str, new_password: str, token_data: dict):
        if not bcrypt_context.verify(current_password, user.password_hash):
            auth_logger.info(token_data)
            raise WrongPasswordError(user_id=token_data['identity'].get('user_id'))

        new_password = self.validator.validate_password(new_password)
        user.password_hash = self.hash_password(new_password)
        self.session.commit()

        self.blocklist.revoke_token(token_data)

        return True


    def authenticate_user_identifier(self, identifier: str):
        """Authenticate a user's identifier without validating a password (for password resets)"""
        user = None

        #Only staff are required to reset a password
        stmt = select(Staff).where(Staff.email_address == identifier.lower())
        user = self.session.execute(stmt).scalars().first()

        if not user:
            raise InvalidCredentialsError(credential=identifier)

        return user


    def request_password_reset(self, user_identifier: str):
        user = self.authenticate_user_identifier(user_identifier)
        token = self.token_list.save_password_token(user_identifier)

        reset_link = f"https://kademia.com/staff/reset-password?token={token}"

        self.email_service.send_staff_reset_link(
            to_email=user.email_address,
            full_name=f"{user.first_name} {user.last_name}",
            reset_url=reset_link
        )


    def reset_password(
            self, password_token: str, user_identifier: str, new_password: str
                    ):
        user = self.authenticate_user_identifier(user_identifier)

        if not self.token_list.is_token_active(password_token):
            raise ResetLinkExpiredError(token = password_token)

        new_password = self.validator.validate_password(new_password)
        user.password_hash = self.hash_password(new_password)
        self.session.commit()

        try:
            self.token_list.redis.delete(f"{self.token_list.key_pref}{password_token}")
            return True
        except Exception as redis_error:
            auth_logger.error(
                f"Password was reset but token revocation failed for user {user_identifier}: {redis_error}"
            )




    def forgot_password(self, identifier: str, user_type: UserType):
        password = self.generate_random_password()

        if user_type == UserType.GUARDIAN:
            stmt = (
                select(Guardian)
                .where(Guardian.email_address == identifier)
            )
            guardian = self.session.execute(stmt).scalar_one_or_none()

            if not guardian:
                raise InvalidCredentialsError(credential=identifier)

            guardian.password_hash = self.hash_password(password)

            full_name = f"{guardian.title}. {guardian.last_name}"
            self.email_service.send_guardian_new_password(
                guardian.email_address, full_name, password)

            self.session.commit()

        elif user_type == UserType.STUDENT:
            stmt = (
                select(Student)
                .where(Student.student_id == identifier)
            )
            student = self.session.execute(stmt).scalar_one_or_none()

            if not student:
                raise InvalidCredentialsError(credential=identifier)

            guardian = self.session.execute(
                select(Guardian)
                .where(Guardian.id == student.guardian_id)
                ).scalar_one_or_none()

            student.password_hash = self.hash_password(password)

            full_name = f"{guardian.title}. {guardian.last_name}"

            self.email_service.send_ward_password_change_notification(
                guardian.email_address, full_name, password,
                student.first_name, student.last_name)

            self.session.commit()




