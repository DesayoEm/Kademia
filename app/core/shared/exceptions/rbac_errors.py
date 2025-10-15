from .base_error import KademiaError

class RoleError(KademiaError):
    """Base exception for all RBAC-related exceptions"""

class NegativeRankError(RoleError):
    """Raised when a negative number is entered as a role rank"""
    def __init__(self, value: int):
        super().__init__()
        self.user_message = "Rank cannot be negative"
        self.log_message = f"Negative number entry attempted on role: {str(value)}"


class NoMatchingRoleError(RoleError):
    """Raised when no matching role is found after a name search"""
    def __init__(self, role_name: str, error_message: str):
        super().__init__()
        self.user_message = f"No matching role found for {role_name}"
        self.log_message = f"No matching role found for {role_name}. Error: {error_message}"