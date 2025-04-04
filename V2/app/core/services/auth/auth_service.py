from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func
from .password_service import bcrypt_context
from ...errors.auth_errors import InvalidCredentialsError
from ....database.models.users import Staff, Guardian, Student
from ....database.models.enums import UserType
from .token_service import TokenService
from datetime import timedelta, datetime


class AuthService:
    def __init__(self, session: Session):
        self.session = session
        self.token_service = TokenService()

    def authenticate_user(self, identifier: str, password: str, user_type: UserType):
        """Authenticate a user based on their type"""
        user = None

        if user_type == UserType.STUDENT:
            stmt = select(Student).where(func.lower(Student.student_id) == identifier.lower())
            user = self.session.execute(stmt).scalars().first()

        elif user_type == UserType.GUARDIAN:
            stmt = select(Guardian).where(
                or_(
                    Guardian.email_address == identifier.lower(),
                    Guardian.phone == identifier
                )
            )
            user = self.session.execute(stmt).scalars().first()

        elif user_type == UserType.STAFF:
            stmt = select(Staff).where(Staff.email_address == identifier.lower())
            user = self.session.execute(stmt).scalars().first()

        if not user:
            raise InvalidCredentialsError(credential=identifier)
        if not bcrypt_context.verify(password, user.password_hash):
            raise InvalidCredentialsError(credential=identifier)

        user.last_login = datetime.now()
        self.session.commit()
        return user


    def authenticate_user_identifier(self, identifier: str):
        """Authenticate a user's identifier without validating a password (for password resets)"""
        user = None

        #Only staff are required to reset a password
        stmt = select(Staff).where(Staff.email_address == identifier.lower())
        user = self.session.execute(stmt).scalars().first()

        if not user:
            raise InvalidCredentialsError(credential=identifier)

        return user


    def log_in(self, identifier: str, password: str, user_type: UserType):
        """Login a user and generate access tokens"""
        user = self.authenticate_user(identifier, password, user_type)
        user_data = {
            "user_id": str(user.id),
            "user_type": user_type.value,
            "access_level": user.access_level,
        }

        if user_type == UserType.STAFF:
            user_data.update({
                "staff_type": user.staff_type,
            })


        access_token = self.token_service.create_access_token(
            user_data = user_data,
            expiry = timedelta(minutes=30)
        )

        refresh_token = self.token_service.create_access_token(
            user_data=user_data,
            refresh=True,
            expiry=timedelta(days=1)
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_type": user_type
        }


