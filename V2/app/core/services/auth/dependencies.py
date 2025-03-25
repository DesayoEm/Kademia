from .token_service import TokenService
from fastapi.security import HTTPBearer
token_service = TokenService()

class AccessTokenBearer(HTTPBearer):
    pass

  