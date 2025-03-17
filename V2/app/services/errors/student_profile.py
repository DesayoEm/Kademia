from .base_error import KademiaError
from .input_errors import TextTooShortError, EmptyFieldError, BlankFieldError


class ProfileError(KademiaError):
    """
    Base exception class for all exceptions related to profile data..
    """
    DOMAIN = "Profiles"

# Domain-specific extensions of input errors
class StaffEmptyFieldError(EmptyFieldError):
    def __init__(self, input_value: str):
        super().__init__(data=input_value, domain=ProfileError.DOMAIN)

class StaffBlankFieldError(BlankFieldError):
    def __init__(self, input_value: str):
        super().__init__(data=input_value, domain=ProfileError.DOMAIN)

class StaffTextTooShortError(TextTooShortError):
    def __init__(self, input_value: str, min_length=3):
        super().__init__(data=input_value, min_length=min_length, domain=ProfileError.DOMAIN)


class DuplicateStudentIDError(ProfileError):
    def __init__(self, stu_id):
        self.stu_id = stu_id
        super().__init__(f'A student with id {stu_id} already exists')

class StudentNotFoundError(ProfileError):
    def __init__(self):
        super().__init__(f'Student not found!')

class StudentIdFormatError(ProfileError):
    def __init__(self):
        super().__init__("Please use correct id format (STU/00/00/0000)")

class IdYearError(ProfileError):
    def __init__(self):
        super().__init__("Academic years in student_id must be consecutive e.g (STU/10/11/0000)")

class DateError(ProfileError):
    def __init__(self):
        super().__init__('Admission date cannot be in the future')


