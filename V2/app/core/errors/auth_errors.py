from .base_error import KademiaError

class AuthError(KademiaError):
    """Base exception for all authorization and authentication-related errors"""

class InvalidUserError(AuthError):
    def __init__(self, email_address: str):
        self.user_message = "Invalid email or password"
        self.log_message = f"Login attempted with Invalid email or password: User {email_address} "
        super().__init__()


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