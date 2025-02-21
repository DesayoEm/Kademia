from .base_error import TrakademikError

class StaffOrganizationError(TrakademikError):
    """
    Base exception class for all exceptions related to staff organization.
    Inherits from TrakademikError.
    """
    pass

class EmptyNameError(StaffOrganizationError):
    """Raised when a name field is empty."""
    def __init__(self):
        super().__init__('Name cannot be empty')

class BlankNameError(StaffOrganizationError):
    """Raised when a name field is blank (contains only whitespace)."""
    def __init__(self):
        super().__init__('Name cannot be blank')

class NameTooShortError(StaffOrganizationError):
    """Raised when a name is too short, specifically when it has two or fewer characters."""
    def __init__(self):
        super().__init__('Name must be greater than three characters')
