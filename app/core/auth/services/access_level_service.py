from uuid import UUID
from sqlalchemy.orm import Session
from app.core.shared.models.enums import UserRole



class AccessLevelService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user

