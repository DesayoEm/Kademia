from .config import r
import secrets
from datetime import datetime, timedelta


class PasswordTokenList:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.key_pref = "password_token:"
        self.exp = timedelta(minutes = 15)

    @staticmethod
    def generate_reset_token():
        return secrets.token_urlsafe(32)

    def save_password_token(self, user_identifier: str):
        token = self.generate_reset_token()
        ttl = int(self.exp.total_seconds())

        key = f"{self.key_pref}{token}"

        self.redis.setex(key, ttl, user_identifier)
        return token


    def is_token_active(self, token) -> bool:
            key = f"{self.key_pref}{token}"
            return self.redis.exists(key) == 1


password_token_list = PasswordTokenList(r)