from V2.app.core.errors.input_errors import (
    EmptyFieldError, BlankFieldError, TextTooShortError
)

class StudentOrganizationValidators:
    def __init__(self):
        pass

    @staticmethod
    def validate_name(value:str) -> str:
        if not value:
            raise EmptyFieldError(data = value)
        if not value.strip():
            raise BlankFieldError(data = value)
        if len(value.strip()) < 3:
            raise TextTooShortError(data = value)
        return value.strip().title()

    @staticmethod
    def validate_description(value:str):
        if not value:
            raise EmptyFieldError(data = value)
        if not value.strip():
            raise BlankFieldError(data = value)
        if len(value.strip()) < 3:
            raise TextTooShortError(data = value)
        return value.strip().capitalize()


