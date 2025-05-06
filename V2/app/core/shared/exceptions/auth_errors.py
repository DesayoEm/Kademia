from .base_error import KademiaError
from uuid import UUID

class AuthError(KademiaError):
    """Base exception for all authorization and authentication-related exceptions"""


class InvalidCredentialsError(AuthError):
    def __init__(self, credential: str):
        self.user_message = "Invalid credentials"
        self.log_message = f"Login attempted with Invalid email or password: User {credential} "
        super().__init__()


class WrongPasswordError(AuthError):
    def __init__(self, user_id: UUID):
        self.user_message = "Password does not match our records"
        self.log_message = f"User: {user_id} attempted password change with wrong password"
        super().__init__()


class PasswordFormatError(AuthError):
    def __init__(self):
        self.user_message = ("Password must meet all the following criteria:\n"
                "- Must be between 8 and 12 characters \n"
                "- Must contain at least one uppercase letter  \n"
                "- Must contain at least one lowercase letter\n"
                "- Must contain at least one number\n"
                "- Must contain at least one special character"
                )
        self.log_message = f"Password setting attempted with invalid format "
        super().__init__()


class UserNotFoundError(AuthError):
    """Raised when a identity account is not found."""

    def __init__(self, identifier: str):
        self.user_message = f"User not found!"
        self.log_message = f"Staff with id:{identifier} not found."


#Token related exceptions
class TokenError(AuthError):
    """Base exception for all token-related exceptions"""

class TokenExpiredError(TokenError):
    """Raised when a token has expired"""

    def __init__(self, error: str):
        self.user_message = "Session expired"
        self.log_message = f"Authentication token expired. Detail:{error} "
        super().__init__()


class ResetLinkExpiredError(TokenError):
    """Raised when a password reset token has expired"""

    def __init__(self, token: str):
        self.user_message = "Reset link expired!"
        self.log_message = f"Password reset token expired. Detail:{token} "
        super().__init__()


class TokenInvalidError(TokenError):
    """Raised when the token is invalid"""
    def __init__(self, error: str):
        self.user_message = "Invalid authentication token"
        self.log_message = f"Invalid authentication token. Detail:{error} "
        super().__init__()


class AccessTokenRequiredError(TokenError):
    """Raised when """
    def __init__(self):
        self.user_message = "Access token required, received refresh token"
        self.log_message = f"Access token required, received refresh token"
        super().__init__()


class RefreshTokenRequiredError(TokenError):
    """Raised when """
    def __init__(self):
        self.user_message = "Refresh token required, received access token"
        self.log_message = f"Refresh token required, received access token"
        super().__init__()


class TokenRevokedError(TokenError):
    """Raised when """
    def __init__(self, jti):
        self.user_message = "Token has been revoked"
        self.log_message = f"Token id {jti} has been revoked"
        super().__init__()

#Access Level Errors
class SameLevelError(AuthError):
    """Raised when """
    def __init__(self, new, previous):
        super().__init__()
        self.user_message = "Previous level and new level cannot be the same"
        self.log_message = (f"Access level with previous and new levels attempted.\
            Previous: {previous} New: {new}")
