from .base_error import KademiaError
from uuid import UUID


class StudentOrganizationError(KademiaError):
    """Base exception class for all exceptions related to student organization."""


class InvalidCodeError(StudentOrganizationError):
    """Raised when a department code string has fewer or more than the required characters."""

    def __init__(self, entry: str, length, domain=None):
        super().__init__()
        self.user_message = f"Code has to be exactly {length} alphabetical characters!"
        self.log_message = (
            f"Domain: {domain}-- Input attempted with Invalid length: {entry}"
        )


class InvalidOrderNumberError(StudentOrganizationError):
    """Raised when an order number fails validation."""

    def __init__(self, entry: int, domain=None):
        super().__init__()
        self.user_message = f"Order must be greater than 0!"
        self.log_message = (
            f"Domain: {domain}-- Order entry attempted with Invalid integer: {entry}"
        )


class InvalidRankNumberError(StudentOrganizationError):
    """Raised when a promotion rank number fails validation."""

    def __init__(self, entry: int, domain=None):
        super().__init__()
        self.user_message = f"Rank must be greater than 0!"
        self.log_message = f"Domain: {domain}-- Promotion rank entry attempted with Invalid integer: {entry}"


class ClassLevelMismatchError(StudentOrganizationError):
    def __init__(self, stu_id: UUID, class_id: UUID):
        self.user_message = (
            f"Student cannot be assigned to a class outside their academic level"
        )
        self.log_message = (
            f"Student {stu_id} assigned a class {class_id} outside their level"
        )


class ClassRepMismatchError(StudentOrganizationError):
    def __init__(self, stu_id: UUID, class_id: UUID):
        self.user_message = (
            f"Student cannot be assigned to represent a class they dont belong to"
        )
        self.log_message = (
            f"Student {stu_id} assigned a class {class_id} they dont belong to"
        )


class DepartmentRepMismatchError(StudentOrganizationError):
    def __init__(self, stu_id: UUID, department_id: UUID):
        self.user_message = (
            f"Student cannot be assigned to represent a department they dont belong to"
        )
        self.log_message = f"Student {stu_id} assigned a department {department_id} they dont belong to"
