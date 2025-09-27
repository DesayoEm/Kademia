from uuid import UUID
from sqlalchemy.orm import Session, selectinload
from typing import List
from app.core.shared.exceptions import EntityNotFoundError
from app.core.shared.exceptions.auth_errors import SameRoleError
from app.core.rbac.models import Role, Permission


class RoleChangeService:
    def __init__(self):
        pass

    @staticmethod
    def prevent_redundant_changes(
            current_role_id: UUID, new_role_id: UUID) -> UUID:
        if current_role_id == new_role_id:
            raise SameRoleError(previous=current_role_id, new=new_role_id)

        return new_role_id


    def see_role_permissions(self, role_id: UUID) -> List[Permission]:
        role = (
            self.session.query(Role)
            .options(selectinload(Role.permissions))
            .filter(Role.id == role_id)
            .first()
        )
        if not role:
            raise EntityNotFoundError(
                Role, role_id, "Role not found", "role"
            )

        return role.permissions


