from ...services.errors.staff_organisation_errors import (
    EmptyFieldError, BlankFieldError, TextTooShortError
)

class StaffOrganizationValidators:
    def _init__(self):
        pass

    @staticmethod
    def validate_name(value:str) -> str:
        if not value:
            raise EmptyFieldError(input = value)
        if not value.strip():
            raise BlankFieldError(input = value)
        if len(value.strip()) < 3:
            raise TextTooShortError(input = value)
        return value.strip().title()

    @staticmethod
    def validate_description(value:str):
        if not value:
            raise EmptyFieldError(input = value)
        if not value.strip():
            raise BlankFieldError(input = value)
        return value.strip().capitalize()

