from datetime import datetime, timedelta, timezone
import jwt
import uuid

from app.core.shared.exceptions import TokenInvalidError, TokenExpiredError
from app.settings import config


class TokenService:
    """
    Service for creating, decoding, and refreshing JWT tokens.

    Handles both access tokens (short-lived) and refresh tokens (longer-lived)
    using PyJWT. Tokens include a unique identifier (jti) for revocation support
    and an identity payload containing user data.

    Attributes:
        ACCESS_TOKEN_EXPIRY: Default token expiry in seconds, loaded from config.

    Token Payload Structure:
        - identity (dict): User data (user_id, user_type, current_role_id, etc.)
        - exp (datetime): Expiration timestamp.
        - jti (str): Unique token identifier (UUID) for blocklist/revocation.
        - refresh (bool): Flag indicating if this is a refresh token.
    """

    def __init__(self):
        """
        Initialize the TokenService.

        No dependencies required; configuration is loaded from app settings.
        """

    ACCESS_TOKEN_EXPIRY = config.ACCESS_TOKEN_EXPIRE_SECONDS

    def create_access_token(
        self, user_data: dict, expiry: timedelta = None, refresh: bool = False
    ):
        """
        Generate a signed JWT token with the provided user data.

        Args:
            user_data: Dict of user information to embed in the token's identity
                claim. Typically includes user_id, user_type, and current_role_id.
            expiry: Optional timedelta for token lifetime. Defaults to
                ACCESS_TOKEN_EXPIRY from config if not provided.
            refresh: If True, marks this token as a refresh token. Refresh tokens
                typically have longer expiry and are used to obtain new access tokens.

        Returns:
            str: The encoded JWT token string.

        Example:
            access_token = token_service.create_access_token(
                user_data={"user_id": "123", "user_type": "staff"},
                expiry=timedelta(minutes=30)
            )
            refresh_token = token_service.create_access_token(
                user_data={"user_id": "123", "user_type": "staff"},
                expiry=timedelta(days=1),
                refresh=True
            )
        """
        payload = {}

        payload["identity"] = user_data
        payload["exp"] = datetime.now() + (
            expiry
            if expiry is not None
            else timedelta(seconds=self.ACCESS_TOKEN_EXPIRY)
        )
        payload["jti"] = str(uuid.uuid4())
        payload["refresh"] = refresh

        token = jwt.encode(
            payload=payload, key=config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
        )
        return token

    def decode_token(self, token: str) -> dict:
        """
        Decode and validate a JWT token.

        Verifies the token signature and expiration using the configured
        secret and algorithm.

        Args:
            token: The encoded JWT token string to decode.

        Returns:
            dict: The decoded token payload containing identity, exp, jti,
                and refresh claims.

        Raises:
            TokenExpiredError: If the token's exp claim is in the past.
            TokenInvalidError: If the token signature is invalid, malformed,
                or fails any other validation.
        """
        try:
            decoded_token = jwt.decode(
                jwt=token, key=config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
            )
            return decoded_token
        except jwt.ExpiredSignatureError as e:
            raise TokenExpiredError(str(e))
        except jwt.InvalidTokenError as e:
            raise TokenInvalidError(str(e))
        except jwt.PyJWTError as e:
            raise TokenInvalidError(str(e))

    def refresh_token(self, token_details):
        """
        Generate a new access token from valid refresh token details.

        Validates that the provided token has not expired, then creates a fresh
        access token with the same identity data and default expiry.

        Args:
            token_details: The decoded refresh token payload (from decode_token),
                must contain 'exp' and 'identity' keys.

        Returns:
            str: A new encoded access token string.

        Raises:
            TokenInvalidError: If the refresh token has expired.

        Note:
            This method expects already-decoded token data. Call decode_token()
            first to validate and decode the raw refresh token string.
        """
        expiry = token_details["exp"]
        if datetime.fromtimestamp(expiry, tz=timezone.utc) > datetime.now(
            tz=timezone.utc
        ):
            new_access_token = self.create_access_token(
                user_data=token_details["identity"]
            )
            return new_access_token
        raise TokenInvalidError
