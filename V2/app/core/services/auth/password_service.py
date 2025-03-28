import random
import string
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ...errors.auth_errors import WrongPasswordError
from ...validators.users import UserValidator
from ....database.redis.tokens import token_blocklist
from ....database.models.users import Staff, Guardian, Student
from ....database.models.enums import UserType

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class PasswordService:

    def __init__(self, session: Session):
        self.session = session
        self.blocklist = token_blocklist
        self.validator = UserValidator()

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
        return password


    @staticmethod
    def hash_password(password: str):
        hashed_password = bcrypt_context.hash(password)
        return hashed_password

    def change_password(self, user, current_password, new_password, token_data):
        if not bcrypt_context.verify(current_password, user.password_hash):
            raise WrongPasswordError
        new_password = self.validator.validate_password(new_password)
        user.password_hash = self.hash_password(new_password)
        self.session.commit()
        self.blocklist.revoke_token(token_data)

        return True


    def forgot_password(self, identifier):
        user = None
        if '@school' in identifier:
            pass
            #user = query staff
        elif '@' in identifier:
            pass
            # user = query guardians
        else:
            pass
            #query students
        if not user:
            pass
            #raise error
        password = self.generate_random_password()
        user.password_hash = self.hash_password(password)
        if user.user_type == UserType.STUDENT:
            guardian = self.session.query(Guardian).filter(
                Guardian.id == user.guardian_id.first()
            )
            #send email to guardian
            #commit session

        elif user.user_type == UserType.GUARDIAN:
            pass
            #send reset email to owner
            # commit session

        elif user.user_type == UserType.STAFF:
            pass
            #Send reset link

