from uuid import UUID
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from typing import List
from app.core.shared.exceptions import EntityNotFoundError
from app.core.shared.exceptions.auth_errors import SameRoleError
from app.core.shared.exceptions import NoMatchingRoleError
from app.core.shared.models.enums import UserRoleName
from app.core.rbac.models import Role, Permission


class RBACService:
    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def prevent_redundant_changes(current_role_id: UUID, new_role_id: UUID) -> UUID:
        if current_role_id == new_role_id:
            raise SameRoleError(previous=current_role_id, new=new_role_id)

        return new_role_id

    def fetch_role_id(self, role_name: str) -> UUID:
        try:
            stmt = select(Role).where(Role.name == UserRoleName[role_name])
            role_obj = self.session.execute(stmt).scalar_one()
            role_id = role_obj.id
            return role_id

        except NoResultFound as e:
            raise NoMatchingRoleError(role_name, str(e))

    def get_role_permission_strs(self, role_id: UUID) -> List[Permission]:
        role = (
            self.session.query(Role)
            .options(selectinload(Role.permissions))
            .filter(Role.id == role_id)
            .first()
        )
        if not role:
            raise EntityNotFoundError(Role, role_id, "Role not found", "role")

        permissions = role.permissions
        return [permission.name for permission in permissions]
