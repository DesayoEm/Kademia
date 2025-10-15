
from uuid import UUID
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.shared.exceptions import NoMatchingRoleError
from app.core.shared.models.enums import UserRoleName
from app.core.rbac.models import Role


class RBACService:
    def __init__(self, session: Session):
        self.session = session


    def fetch_role_id(self, role_name: str) -> UUID:
        try:
            stmt = select(Role).where(Role.name == UserRoleName[role_name])
            role_obj = self.session.execute(stmt).scalar_one()
            role_id = role_obj.id
            return role_id

        except NoResultFound as e:
            raise NoMatchingRoleError(role_name, str(e))