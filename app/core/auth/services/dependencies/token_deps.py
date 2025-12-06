from fastapi.security import HTTPBearer
from fastapi import Request
from sqlalchemy.orm import Session

from app.core.shared.exceptions import (
    RefreshTokenRequiredError,
    TokenRevokedError,
    AccessTokenRequiredError,
)
from app.infra.db.redis_db.access_tokens import token_blocklist
from app.core.auth.services.token_service import TokenService

token_service = TokenService()
session = Session()


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super().__call__(request)
        token = credentials.credentials
        token_data = token_service.decode_token(token)

        if token_blocklist.is_token_revoked(token_data):
            raise TokenRevokedError(jti=token_data["jti"])

        self.verify_token_data(token_data)

        return token_data

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override in child classes")


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data.get("refresh", False):
            raise AccessTokenRequiredError


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get("refresh", False):
            raise RefreshTokenRequiredError


access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
