import random
import string
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class PasswordService:

    def __init__(self):
        pass

    @staticmethod
    def generate_random_password():
        length = 10
        characters = list(string.ascii_letters + string.digits + "!@#$%&")
        random.shuffle(characters)
        password = []
        for item in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        password = "".join(password)
        print(password)
        return password


    @staticmethod
    def hash_password(password: str):
        hashed_password = bcrypt_context.hash(password)
        return hashed_password

