from .base_error import KademiaError
from uuid import UUID


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


class AccessDenied(RoleError):
    """Raised when a user tries to access a resource they don't have permissions to"""
    def __init__(self, user_id: UUID, resource_id: UUID, permission: str):
        super().__init__()
        self.user_message = f"Access denied. \nCheck with you administrator if you think you should be a able to access this record"
        self.log_message = f"Access denied for {user_id}. \n Error: Tried to {permission} on {resource_id}"