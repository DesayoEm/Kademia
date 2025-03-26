from .token_service import TokenService
from fastapi.security import HTTPBearer
from fastapi import Request

from ...errors.auth_errors import RefreshTokenRequiredError
from ....core.errors.auth_errors import AccessTokenRequiredError

token_service = TokenService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)


    async def __call__(self, request: Request):
        print(f"Called from: {self.__class__.__name__}")
        credentials = await super().__call__(request)
        token = credentials.credentials
        token_data = token_service.decode_token(token)
        self.verify_token_data(token_data)

        return token_data

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override in child classes")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data.get('refresh', False):
                raise AccessTokenRequiredError


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data.get('refresh', False):
                raise RefreshTokenRequiredError


 #