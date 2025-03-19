from datetime import datetime, timedelta
from ....core.errors.auth_errors import TokenInvalidError, TokenExpiredError
from ....config import config
import jwt
import uuid

class TokenService:
    def __init__(self):
        pass

    ACCESS_TOKEN_EXPIRY = 3600

    def create_access_token(self, user_data: dict, expiry:timedelta = None,
                            refresh: bool=False):
        payload = {}

        payload['user']=user_data
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


