from sqlalchemy.orm import Session
from .password_service import bcrypt_context
from ...errors.auth_errors import InvalidUserError
from ....database.models.users import Staff, Guardians, Students

class AuthService:
    def __init__(self, session: Session):
        self.session = session

    def authenticate_staff(self, email_address: str, password: str):
        staff = self.session.query(Staff).filter(Staff.email_address == email_address.lower()
                        ).first()
        if not staff:
            raise InvalidUserError(email_address=email_address)
        if not bcrypt_context.verify(password, staff.password_hash):
            raise InvalidUserError(email_address=email_address)
        return staff
