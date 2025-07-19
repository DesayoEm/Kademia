from datetime import datetime, timedelta, timezone
import jwt
import uuid

from app.core.shared.exceptions import TokenInvalidError, TokenExpiredError
from app.infra.settings import config

class TokenService:
    def __init__(self):
        pass

    ACCESS_TOKEN_EXPIRY = config.ACCESS_TOKEN_EXPIRE_SECONDS

    def create_access_token(self, user_data: dict, expiry:timedelta = None,
                            refresh: bool=False):
        payload = {}

        payload['identity']=user_data
        payload['exp']=datetime.now() + (
            expiry if expiry is not None else timedelta(seconds=self.ACCESS_TOKEN_EXPIRY))
        payload['jti']=str(uuid.uuid4())
        payload['refresh']=refresh

        token = jwt.encode(
            payload = payload,
            key = config.JWT_SECRET,
            algorithm = config.JWT_ALGORITHM
        )
        return token


    def decode_token(self, token: str) -> dict:
        try:
            decoded_token = jwt.decode(
            jwt=token,
            key=config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITHM]
        )
            return decoded_token
        except jwt.ExpiredSignatureError as e:
            raise TokenExpiredError(str(e))
        except jwt.InvalidTokenError as e:
            raise TokenInvalidError(str(e))
        except jwt.PyJWTError as e:
            raise TokenInvalidError(str(e))


    def refresh_token(self, token_details):
        expiry = token_details['exp']
        if datetime.fromtimestamp(expiry, tz=timezone.utc) > datetime.now(tz=timezone.utc):
            new_access_token = self.create_access_token(
                user_data=token_details['identity']
            )
            return new_access_token
        raise TokenInvalidError
