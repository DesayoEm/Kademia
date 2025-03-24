from .base_error import KademiaError

class AuthError(KademiaError):
    """Base exception for all authorization and authentication-related errors"""

class InvalidCredentialsError(AuthError):
    def __init__(self, credential: str):
        self.user_message = "Invalid credentials"
        self.log_message = f"Login attempted with Invalid email or password: User {credential} "
        super().__init__()

class UserNotFoundError(AuthError):
    """Raised when a user account is not found."""
    def __init__(self, identifier: str):
        self.user_message = f"User not found!"
        self.log_message = f"Staff with id:{identifier} not found."


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