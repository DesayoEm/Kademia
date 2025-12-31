from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.shared.exceptions.auth_errors import TokenInvalidError, UserNotFoundError
from app.core.identity.models.guardian import Guardian
from app.core.identity.models.staff import Staff
from app.core.identity.models.student import Student
from app.core.shared.schemas.enums import UserType
from app.core.auth.services.token_service import TokenService
from app.infra.db.session_manager import get_db

token_service = TokenService()
access = AccessTokenBearer()

"""
FastAPI dependency injection utilities for authentication and service instantiation.

Provides factory functions for creating route dependencies that automatically
handle database sessions, token validation, and user resolution. Enables
consistent authentication patterns across routes without boilerplate.

Module Attributes:
    token_service: Shared TokenService instance for JWT operations.
    access: AccessTokenBearer dependency for extracting/validating tokens.

"""

def get_current_user(token_data, db_session):
    """
    Resolve token data to a user model instance.

    Extracts user_id and user_type from the token's identity claim, then
    queries the appropriate table (Staff, Student, or Guardian) to fetch
    the full user object.

    Args:
        token_data: Decoded JWT payload containing an 'identity' dict with
            'user_id' and 'user_type' keys.
        db_session: Active SQLAlchemy session for database queries.

    Returns:
        The user model instance (Staff, Student, or Guardian).

    Raises:
        TokenInvalidError: If the token is missing user_id or user_type.
        UserNotFoundError: If no user exists with the given ID in the
            expected table.
    """
    user_data = token_data["identity"]

    user_id = user_data.get("user_id")
    user_type = user_data.get("user_type")

    if not user_id or not user_type:
        raise TokenInvalidError(error="Invalid token structure")

    user = None
    if user_type == UserType.STAFF:
        user = db_session.query(Staff).filter(Staff.id == user_id).first()
    elif user_type == UserType.STUDENT:
        user = db_session.query(Student).filter(Student.id == user_id).first()
    elif user_type == UserType.GUARDIAN:
        user = db_session.query(Guardian).filter(Guardian.id == user_id).first()

    if user is None:
        raise UserNotFoundError(identifier=user_id)

    return user


def get_authenticated_factory(factory_class):
    """
    Create a FastAPI dependency that provides an authenticated factory instance.

    Returns a dependency function that resolves the current user from the
    access token and instantiates the given factory class with the database
    session and authenticated user.

    Args:
        factory_class: A factory class whose __init__ accepts (session, current_user).

    Returns:
        Callable: A FastAPI-compatible dependency function.

    """

    def get_factory(
        session: Session = Depends(get_db), token_data: dict = Depends(access)
    ):
        current_user = get_current_user(token_data, session)
        return factory_class(session, current_user=current_user)

    return get_factory


def get_authenticated_service(service_class):
    """
    Create a FastAPI dependency that provides an authenticated service instance.

    Returns a dependency function that resolves the current user from the
    access token and instantiates the given service class with the database
    session and authenticated user.

    Args:
        service_class: A service class whose __init__ accepts (session, current_user).

    Returns:
        Callable: A FastAPI-compatible dependency function.

    """

    def get_service(
        session: Session = Depends(get_db), token_data: dict = Depends(access)
    ):
        current_user = get_current_user(token_data, session)
        return service_class(session, current_user=current_user)

    return get_service



