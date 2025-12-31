from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func
from datetime import timedelta, datetime
from .password_service import bcrypt_context

from app.core.shared.exceptions import InvalidCredentialsError
from .token_service import TokenService
from app.core.identity.models.guardian import Guardian
from app.core.identity.models.staff import Staff
from app.core.identity.models.student import Student
from app.core.shared.schemas.enums import UserType


class AuthService:
    """
    Authentication service for handling user login and credential verification.

    This service supports authentication for three user types: students, guardians,
    and staff members. Each user type has different identifier lookup strategies:
    - Students: matched by student_id (case-insensitive)
    - Guardians: matched by email address or phone number
    - Staff: matched by email address

    Attributes:
        session: SQLAlchemy database session for executing queries.
        token_service: TokenService instance for generating JWT tokens.

    Example:
        auth_service = AuthService(db_session)
        tokens = auth_service.log_in("a@a.edu", "password123", UserType.STAFF)
    """

    def __init__(self, session: Session):
        """
        Initialize the AuthService with a database session.

        Args:
            session: An active SQLAlchemy Session instance for database operations.
        """
        self.session = session
        self.token_service = TokenService()

    def authenticate_user(self, identifier: str, password: str, user_type: UserType):
        """
        Verify user credentials and return the authenticated user object.
        Looks up the user by identifier based on user_type, verifies the password against the stored bcrypt hash,
        and updates the user's last_login timestamp on successful authentication.

        Args:
        identifier: The login identifier. Interpreted based on user_type:
            - STUDENT: student_id (case-insensitive)
            - GUARDIAN: email address or phone number
            - STAFF: email address (case-insensitive)
        password: The plaintext password to verify.
        user_type: A UserType enum indicating which user table to query.

        Returns:
            The authenticated user model instance (Student, Guardian, or Staff).

        Raises:
            InvalidCredentialsError: If no user is found with the given identifier, or if the password does not match.
        """
        user = None

        if user_type == UserType.STUDENT:
            stmt = select(Student).where(
                func.lower(Student.student_id) == identifier.lower()
            )
            user = self.session.execute(stmt).scalars().first()

        elif user_type == UserType.GUARDIAN:
            stmt = select(Guardian).where(
                or_(
                    Guardian.email_address == identifier.lower(),
                    Guardian.phone == identifier,
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
        """
        Authenticate a user and generate access and refresh tokens.

        Wraps authenticate_user() and generates JWT tokens for the authenticated
        session. The token payload includes user_id, user_type, and current_role_id.
        Staff users additionally have staff_type included in the payload.

        Args:
            identifier: The login identifier (student_id, email, or phone).
            password: The plaintext password to verify.
            user_type: A UserType enum indicating the type of user logging in.

        Returns:
            dict: A dictionary containing:
                - access_token (str): Short-lived JWT for API access.
                - refresh_token (str): Longer-lived JWT for token refresh.
                - token_type (str): Always "bearer".
                - user_type (UserType): The authenticated user's type.

        Raises:
            InvalidCredentialsError: Propagated from authenticate_user() if
                authentication fails.
        """

        user = self.authenticate_user(identifier, password, user_type)

        user_data = {
            "user_id": str(user.id),
            "user_type": user_type.value,
            "current_role_id": str(user.current_role_id),
        }

        if user_type == UserType.STAFF:
            user_data.update(
                {
                    "staff_type": user.staff_type,
                }
            )

        access_token = self.token_service.create_access_token(
            user_data=user_data, expiry=timedelta(minutes=30)
        )

        refresh_token = self.token_service.create_access_token(
            user_data=user_data, refresh=True, expiry=timedelta(days=1)
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_type": user_type,
        }
