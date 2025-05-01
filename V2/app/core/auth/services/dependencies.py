from fastapi.security import HTTPBearer
from fastapi import Request
from sqlalchemy.orm import Session

from V2.app.core.shared.exceptions.auth_errors import TokenInvalidError, UserNotFoundError
from V2.app.core.identity.models.guardian import Guardian
from V2.app.core.identity.models.staff import Staff
from V2.app.core.identity.models.student import Student
from V2.app.core.shared.schemas.enums import UserType
from V2.app.core.shared.exceptions import RefreshTokenRequiredError, TokenRevokedError, AccessTokenRequiredError
from V2.app.infra.db.redis.access_tokens import token_blocklist
from .token_service import TokenService

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


def get_current_user(token_data, db_session):
    """Convert token data to a identity object"""

    user_data = token_data["identity"]
    user_id = user_data.get("id")
    user_type = user_data.get("user_type")

    if not user_id or not user_type:
        raise TokenInvalidError(error="Invalid token structure")

    user = None
    if user_type == UserType.STAFF:
        user = db_session.query(Staff).filter(Staff.id == user_id).first()
    elif user_type == UserType.STUDENT:
        user = db_session.query(Student).filter(Student.id == user_id).first()
    elif user_type == UserType.GUARDIAN:
        user = db_session.query(Guardian).filter(Guardian.id == user_id).first()

    if user is None:
        raise UserNotFoundError(identifier=user_id)

    return user