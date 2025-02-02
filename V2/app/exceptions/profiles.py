from .base import ProfileExceptions

class StudentIdFormatError(ProfileExceptions):
    def __init__(self):
        super().__init__("Please use correct id format (STU/00/00/0000)")

class IdYearError(ProfileExceptions):
    def __init__(self):
        super().__init__("Academic years in student_id must be consecutive e.g (STU/10/11/0000)")

