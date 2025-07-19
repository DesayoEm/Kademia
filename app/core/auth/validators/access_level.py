
from app.core.shared.exceptions.auth_errors import SameLevelError
from app.core.shared.schemas.enums import AccessLevel


class AccessLevelValidator:
    def __init__(self):
        self.domain = "Access Level"

    @staticmethod
    def prevent_redundant_changes(
            previous_level: AccessLevel, new_level: AccessLevel) -> AccessLevel:

        if previous_level == new_level:
            raise SameLevelError(previous = previous_level, new = new_level)

        return new_level
