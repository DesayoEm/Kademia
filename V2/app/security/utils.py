from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
class SecurityUtils:

    @staticmethod
    def hash_password(password: str):
        hashed_password = bcrypt_context.hash(password)
        return hashed_password

