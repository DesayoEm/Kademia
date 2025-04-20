from ...core.errors.auth_errors import PasswordFormatError


class AuthValidator:
    def __init__(self):
        self.domain = "AUTH"


    @staticmethod
    def validate_password(password: str):
        is_valid = True

        if not password:
            is_valid = False

        if len(password) < 8 or len(password) > 12:
            is_valid = False

        if not any(char.isupper() for char in password):
            is_valid = False

        if not any(char.islower() for char in password):
            is_valid = False

        if not any(char.isdigit() for char in password):
            is_valid = False

        if not any(not char.isalnum() for char in password):
            is_valid = False

        if not is_valid:
            raise PasswordFormatError()

        return password


