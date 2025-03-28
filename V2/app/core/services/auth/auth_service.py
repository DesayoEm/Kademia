from sqlalchemy.orm import Session
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

    def authenticate_user(
            self, identifier: str, password: str, user_type: UserType):
        """Authenticate a user based on their type"""
        user = None
        if user_type == UserType.STAFF:
            user = self.session.query(Staff).filter(Staff.email_address == identifier.lower()).first()
        elif user_type == UserType.STUDENT:
            user = self.session.query(Student).filter(Student.student_id == identifier).first()
        elif user_type == UserType.GUARDIAN:
            user = self.session.query(Guardian).filter(
                (Guardian.email_address == identifier.lower()) |
                (Guardian.phone == identifier)).first()

        if not user:
            raise InvalidCredentialsError(credential=identifier)
        if not bcrypt_context.verify(password, user.password_hash):
            raise InvalidCredentialsError(credential=identifier)

        user.last_login = datetime.now()
        self.session.commit()
        return user


    def log_in(self, identifier: str, password: str, user_type: UserType):
        """Login a user and generate access tokens"""
        user = self.authenticate_user(identifier, password, user_type)
        user_data = {
            "user_id": str(user.id),
            "user_type": user_type,
            "access_level": user.access_level,
        }

        if user_type == UserType.STAFF:
            user_data.update({
                "email": user.email_address,
                "staff_type": user.staff_type,
            })
        elif user_type == UserType.STUDENT:
            user_data.update({
                "student_id": user.student_id,
            })
        elif user_type == UserType.GUARDIAN:
            user_data.update({
                "email": user.email_address,
                "phone": user.phone
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


