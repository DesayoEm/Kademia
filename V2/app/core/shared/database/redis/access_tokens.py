from .config import r
from datetime import datetime, timedelta
from ...core.errors.auth_errors import TokenInvalidError


class TokenBlocklist:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.key_pref = "revoked_token:"

    def revoke_token(self, token_data: dict):
        jti = token_data.get('jti')
        if not jti:
            raise TokenInvalidError

        exp_timestamp = token_data.get('exp')
        if not exp_timestamp:
            raise TokenInvalidError

        if isinstance(exp_timestamp, (int, float)):
            exp_time = datetime.fromtimestamp(exp_timestamp)
        else:
            exp_time = exp_timestamp

        current_time = datetime.now()
        ttl = max(0, int((exp_time-current_time).total_seconds()))

        key = f"{self.key_pref}:{jti}"
        self.redis.setex(key, ttl, "revoked")

        return True

    def is_token_revoked(self, token_data: dict) -> bool:
        jti = token_data.get('jti')
        if not jti:
            return False
        key = f"{self.key_pref}:{jti}"
        return self.redis.exists(key) == 1

token_blocklist = TokenBlocklist(r)

