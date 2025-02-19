from ..base_exception import TrakademikException

class StaffOrganizationExceptions(TrakademikException):
    """
    Base exception class for all exceptions related to staff organization.
    Inherits from TrakademikException.
    """
    pass

class DuplicateDepartmentError(StaffOrganizationExceptions):
    """
    Raised when an attempt is made to create a department that already exists.
    Attributes:
        dept_name (str): The name of the department that already exists.
    """
    def __init__(self, dept_name):
        self.dept_name = dept_name
        super().__init__(f'A department with name {dept_name} already exists')


class DuplicateRoleError(StaffOrganizationExceptions):
    """
    Raised when an attempt is made to create a role that already exists.
    Attributes:
        role_name (str): The name of the role that already exists.
    """
    def __init__(self, role_name):
        self.role_name = role_name
        super().__init__(f'A role with name {role_name} already exists')


class DuplicateQualificationError(StaffOrganizationExceptions):
    """
    Raised when an attempt is made to create a qualification that already exists.
    Attributes:
        qualification_name (str): The name of the qualification that already exists.
    """
    def __init__(self, qualification_name):
        self.role_name = qualification_name
        super().__init__(f'A qualification with name {qualification_name} already exists')


class DepartmentNotFoundError(StaffOrganizationExceptions):
    """Raised when a department is not found."""
    def __init__(self):
        super().__init__(f'Department not found!')

class RoleNotFoundError(StaffOrganizationExceptions):
    """Raised when a role is not found."""
    def __init__(self):
        super().__init__(f'Role not found!')

class QualificationNotFoundError(StaffOrganizationExceptions):
    """Raised when a qualification is not found."""
    def __init__(self):
        super().__init__(f'Qualification not found!')



class EmptyNameError(StaffOrganizationExceptions):
    """Raised when a name field is empty."""
    def __init__(self):
        super().__init__('Name cannot be empty')

class BlankNameError(StaffOrganizationExceptions):
    """Raised when a name field is blank (contains only whitespace)."""
    def __init__(self):
        super().__init__('Name cannot be blank')

class NameTooShortError(StaffOrganizationExceptions):
    """Raised when a name is too short, specifically when it has three or fewer characters."""
    def __init__(self):
        super().__init__('Name must be greater than three characters')
