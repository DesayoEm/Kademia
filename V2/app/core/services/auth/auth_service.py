from sqlalchemy.orm import Session

from .password_service import bcrypt_context
from ....database.models.users import Staff, Guardians, Students

class AuthService:
    def __init__(self, session: Session):
        self.session = session

    def authenticate_staff(self, email_address: str, password: str):
        staff = self.session.query(Staff).filter(Staff.email_address == email_address
                        ).first()
        if not staff:
            return False
        if not bcrypt_context.verify(password, staff.password_hash):
            return False
        return True
