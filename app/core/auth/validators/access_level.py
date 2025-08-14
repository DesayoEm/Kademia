
from app.core.shared.exceptions.auth_errors import SameLevelError
from app.core.shared.schemas.enums import UserRole


class AccessLevelValidator:
    def __init__(self):
        self.domain = "Access Level"

    @staticmethod
    def prevent_redundant_changes(
            current_role: UserRole, new_role: UserRole) -> UserRole:

        if current_role == new_role:
            raise SameLevelError(previous = current_role, new = new_role)

        return new_role
