from fastapi.security import HTTPBearer
from fastapi import Request, Depends
from ....database.session import get_db
from sqlalchemy.orm import Session
from ...errors.auth_errors import TokenInvalidError, UserNotFoundError
from ....database.models.users import Staff, Guardian, Student
from ....database.models.enums import UserType
from .token_service import TokenService

from ....core.errors.auth_errors import RefreshTokenRequiredError, TokenRevokedError, AccessTokenRequiredError
from ....database.redis.tokens import token_blocklist

token_service = TokenService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)


    async def __call__(self, request: Request):
        print(f"Called from: {self.__class__.__name__}")
        credentials = await super().__call__(request)
        token = credentials.credentials
        token_data = token_service.decode_token(token)

        if token_blocklist.is_token_revoked(token_data):
            raise TokenRevokedError(jti = token_data['jti'])

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


access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()

def get_current_user(
    token_data: dict = Depends(access_token_bearer),
    db: Session = Depends(get_db)
):
    """Convert token data to a user object"""
    user_data = token_data.get("user", {})
    user_id = user_data.get("id")
    user_type = user_data.get("user_type")

    if not user_id or not user_type:
        raise TokenInvalidError(error="Invalid token structure")

    user = None
    if user_type == UserType.STAFF:
        user = db.query(Staff).filter(Staff.id == user_id).first()
    elif user_type == UserType.STUDENT:
        user = db.query(Student).filter(Student.id == user_id).first()
    elif user_type == UserType.GUARDIAN:
        user = db.query(Guardian).filter(Guardian.id == user_id).first()

    if user is None:
        raise UserNotFoundError(identifier=user_id)

    return user