from .base_error import TrakademikError

class StaffOrganizationError(TrakademikError):
    """
    Base exception class for all exceptions related to staff organization.
    Inherits from TrakademikError.
    """
    pass

class DuplicateDepartmentError(StaffOrganizationError):
    """Raised when a duplicate department is created."""
    def __init__(self, name: str, original_error: Exception):
        self.user_message = f"A department with name {name} already exists"
        self.log_message = f"Duplicate department creation attempted: {original_error}"

class DepartmentNotFoundError(StaffOrganizationError):
    """Raised when a department is not found."""
    def __init__(self, name: str, original_error: Exception):
        self.user_message = f"A department with name {name} already exists"
        self.log_message = f"Duplicate department creation attempted: {original_error}"

class DuplicateRoleError(StaffOrganizationError):
    """Raised when a duplicate department is created."""
    def __init__(self, name: str, original_error: Exception):
        self.user_message = f"A class with name {name} already exists"
        self.log_message = f"Duplicate class creation attempted: {original_error}"

class DuplicateQualificationError(StaffOrganizationError):
    """Raised when a duplicate department is created."""
    def __init__(self, name: str, original_error: Exception):
        self.user_message = f"A qualification with name {name} for this educator already exists"
        self.log_message = f"Duplicate department creation attempted: {original_error}"

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
