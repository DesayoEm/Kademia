from V2.app.services.errors.staff_organisation_errors import (
    EmptyNameError, BlankNameError, NameTooShortError
)

class StaffOrganizationValidators:
    def _init__(self):
        pass

    def validate_name(self, value:str) -> str:
        if not value:
            raise EmptyNameError
        if not value.strip():
            raise BlankNameError
        if len(value.strip()) < 3:
            raise NameTooShortError
        return value.strip().capitalize()

    def validate_description(self, value:str):
        if not value:
            raise EmptyNameError
        if not value.strip():
            raise BlankNameError
        return value.strip().capitalize()

staff_organisation_validators = StaffOrganizationValidators()