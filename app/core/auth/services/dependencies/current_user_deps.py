
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

token_service=TokenService()
access = AccessTokenBearer()



def get_current_user(token_data, db_session):
    """Convert token data to a identity object"""
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
    """Factory function to create a dependency that returns a factory class instance with authenticated user"""

    def get_factory(
        session: Session = Depends(get_db),
        token_data: dict = Depends(access)
    ):
        current_user = get_current_user(token_data, session)
        return factory_class(session, current_user=current_user)

    return get_factory


def get_authenticated_service(service_class):
    """Factory function to create a dependency that returns a service class instance with authenticated user"""

    def get_service(
            session: Session = Depends(get_db),
            token_data: dict = Depends(access)
    ):
        current_user = get_current_user(token_data, session)
        return service_class(session, current_user=current_user)

    return get_service


def get_crud(crud_class):
    """Factory function to create a dependency that returns a CRUD instance without authentication"""
    def get_crud(db: Session = Depends(get_db)):
        return crud_class(db)
    return get_crud



def get_authenticated_crud(crud_class):
    """Factory function to create a dependency that returns a CRUD instance with authenticated user"""

    def get_crud(
            db: Session = Depends(get_db),
            token_data: dict = Depends(access)
    ):
        current_user = get_current_user(token_data, db)
        return crud_class(db, current_user = current_user)

    return get_crud


