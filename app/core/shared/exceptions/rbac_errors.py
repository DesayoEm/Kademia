from .base_error import KademiaError

class RoleError(KademiaError):
    """Base exception for all RBAC-related exceptions"""

class NegativeRankError(RoleError):
    """Raised when a negative number is entered as a role rank"""
    def __init__(self, value: int):
        super().__init__()
        self.user_message = "Rank cannot be negative"
        self.log_message = f"Negative number entry attempted on role: {str(value)}"