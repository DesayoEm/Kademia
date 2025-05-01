from .base_error import KademiaError

class StaffOrganizationError(KademiaError):
    """
    Base exception class for all exceptions related to staff organization.
    Inherits from KademiaError.
    """

class LifetimeValidityConflictError(StaffOrganizationError):
    """
    Raised when a 'Lifetime' validity type is selected
       but an invalid date or non-'Lifetime' value is provided for the valid_until field.
    """

    def __init__(self, entry):
        super().__init__()
        self.user_message = f"Valid until field must 'lifetime' if validity type is lifetime"
        self.log_message = f" Lifetime validity Entry attempted with invalid str: {entry}"


class TemporaryValidityConflictError(StaffOrganizationError):
    def __init__(self, entry: str, domain=None):
        super().__init__()
        self.user_message = (
            "If validity type is temporary, "
            "Valid until field must be in the following date format - YYYY-MM-DD"
        )
        self.log_message = f"Domain: {domain}-- Entry attempted with invalid date: {entry}"
