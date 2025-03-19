from jwt.exceptions import PyJWTError, ExpiredSignatureError, InvalidTokenError

class TokenError(Exception):
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