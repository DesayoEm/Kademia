from uuid import UUID
from sqlalchemy.orm import Session
from app.core.shared.models.enums import UserRole
from app.core.shared.exceptions.auth_errors import SameRoleError


class RoleChangeService:
    def __init__(self, session: Session, current_user):
        self.session = session
        self.current_user = current_user

    @staticmethod
    def prevent_redundant_changes(
            current_role: UserRole, new_role: UserRole) -> UserRole:
        if current_role == new_role:
            raise SameRoleError(previous=current_role, new=new_role)

        return new_role

