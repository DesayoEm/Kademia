from uuid import UUID
from sqlalchemy.orm import Session

from app.core.shared.exceptions import NegativeRankError
from app.core.shared.exceptions.auth_errors import SameRoleError


class RoleChangeService:
    def __init__(self, session: Session, current_user=None):
        self.session = session
        self.current_user = current_user

    @staticmethod
    def prevent_redundant_changes(
            current_role_id: UUID, new_role_id: UUID) -> UUID:
        if current_role_id == new_role_id:
            raise SameRoleError(previous=current_role_id, new=new_role_id)

        return new_role_id

    def validate_rank_number(self, value: int)-> int:
        if value < 0:
            raise NegativeRankError(value=value)


