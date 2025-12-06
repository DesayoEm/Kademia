from .base_error import KademiaError
from uuid import UUID


class AuthError(KademiaError):
    """Base exception for all authorization and authentication-related exceptions"""


class SameRoleError(AuthError):
    """Raised when attempting to set a role that is the same as the current one"""

    def __init__(self, new, previous):
        super().__init__()
        self.user_message = "Previous role and new role cannot be the same"
        self.log_message = f"Role change with same previous and new role attempted.\
            Previous: {previous} New: {new}"


class InvalidCredentialsError(AuthError):
    """Raised when provided login credentials are invalid"""

    def __init__(self, credential: str):
        super().__init__()
        self.user_message = "Invalid credentials"
        self.log_message = (
            f"Login attempted with Invalid email or password: User {credential} "
        )


class WrongPasswordError(AuthError):
    """Raised when a user attempts to change password with incorrect current password"""

    def __init__(self, user_id: UUID):
        super().__init__()
        self.user_message = "Password does not match our records"
        self.log_message = (
            f"User: {user_id} attempted password change with wrong password"
        )


class CurrentPasswordError(AuthError):
    """Raised when a user attempts to change their password to the same as their current one"""

    def __init__(self, user_id: UUID):
        super().__init__()
        self.user_message = "You can't change to current password"
        self.log_message = (
            f"User: {user_id} attempted password change to current password"
        )


class PasswordFormatError(AuthError):
    """Raised when a password doesn't meet the required format criteria"""

    def __init__(self):
        self.user_message = (
            "Password must meet all the following criteria:\n"
            "- Must be between 8 and 12 characters \n"
            "- Must contain at least one uppercase letter  \n"
            "- Must contain at least one lowercase letter\n"
            "- Must contain at least one number\n"
            "- Must contain at least one special character"
        )
        self.log_message = f"Password setting attempted with invalid format "
        super().__init__()


class UserNotFoundError(AuthError):
    """Raised when user account is not found"""

    def __init__(self, identifier: str):
        self.user_message = f"User not found!"
        self.log_message = f"Staff with id:{identifier} not found."


# Token related exceptions
class TokenError(AuthError):
    """Base exception for all token-related exceptions"""


class ResetLinkExpiredError(TokenError):
    """Raised when a password reset token has expired"""

    def __init__(self, token: str):
        self.user_message = "Reset link expired!"
        self.log_message = f"Password reset token expired. Detail:{token} "
        super().__init__()


class InvalidPasswordTokenError(TokenError):
    """Raised when a password reset token is invalid"""

    def __init__(self, token: str):
        self.user_message = "Invalid reset link"
        self.log_message = f"Invalid password reset token . Token:{token} "
        super().__init__()


class TokenExpiredError(TokenError):
    """Raised when an authentication token has expired"""

    def __init__(self, error: str):
        self.user_message = "Session expired"
        self.log_message = f"Authentication token expired. Detail:{error} "
        super().__init__()


class TokenInvalidError(TokenError):
    """Raised when an authentication token is invalid"""

    def __init__(self, error: str):
        self.user_message = "Invalid authentication token"
        self.log_message = f"Invalid authentication token. Detail:{error} "
        super().__init__()


class AccessTokenRequiredError(TokenError):
    """Raised when a refresh token is provided where an access token is required"""

    def __init__(self):
        self.user_message = "Access token required, received refresh token"
        self.log_message = f"Access token required, received refresh token"
        super().__init__()


class RefreshTokenRequiredError(TokenError):
    """Raised when an access token is provided where a refresh token is required"""

    def __init__(self):
        self.user_message = "Refresh token required, received access token"
        self.log_message = f"Refresh token required, received access token"
        super().__init__()


class TokenRevokedError(TokenError):
    """Raised when attempting to use a token that has been revoked"""

    def __init__(self, jti):
        self.user_message = "Token has been revoked"
        self.log_message = f"Token id {jti} has been revoked"
        super().__init__()
