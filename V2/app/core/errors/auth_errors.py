from .base_error import KademiaError

class AuthError(KademiaError):
    """Base exception for all authorization and authentication-related errors"""

class InvalidCredentialsError(AuthError):
    def __init__(self, credential: str):
        self.user_message = "Invalid credentials"
        self.log_message = f"Login attempted with Invalid email or password: User {credential} "
        super().__init__()


class WrongPasswordError(AuthError):
    def __init__(self):
        self.user_message = "Wrong password!"
        self.log_message = f"Password change attempted with wrong password "
        super().__init__()


class UserNotFoundError(AuthError):
    """Raised when a user account is not found."""
    def __init__(self, identifier: str):
        self.user_message = f"User not found!"
        self.log_message = f"Staff with id:{identifier} not found."

class EmailFailedToSendError(AuthError):
    """Raised when sending an email fails."""
    def __init__(self, detail: str):
        self.user_message = f"Failed to send email!"
        self.log_message = f"Failed to send email: {detail}."

#Token related errors
class TokenError(AuthError):
    """Base exception for all token-related errors"""

class TokenExpiredError(TokenError):
    """Raised when the token has expired"""
    def __init__(self, error: str):
        self.user_message = "Session expired"
        self.log_message = f"Authentication token expired. Detail:{error} "
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