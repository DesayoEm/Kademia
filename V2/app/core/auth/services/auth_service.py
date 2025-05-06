from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func
from datetime import timedelta, datetime
from .password_service import bcrypt_context

from V2.app.core.shared.exceptions import InvalidCredentialsError
from .token_service import TokenService
from V2.app.core.identity.models.guardian import Guardian
from V2.app.core.identity.models.staff import Staff
from V2.app.core.identity.models.student import Student
from V2.app.core.shared.schemas.enums import UserType


class AuthService:
    def __init__(self, session: Session):
        self.session = session
        self.token_service = TokenService()

    def authenticate_user(self, identifier: str, password: str, user_type: UserType):
        """Authenticate identity based on user type"""
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


    def log_in(self, identifier: str, password: str, user_type: UserType):
        """Login a identity and generate access tokens"""
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


