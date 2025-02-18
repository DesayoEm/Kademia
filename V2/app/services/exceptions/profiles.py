from V2.app.services.base_exception import ProfileExceptions
class DuplicateStudentIDError(ProfileExceptions):
    def __init__(self, stu_id):
        self.stu_id = stu_id
        super().__init__(f'A student with id {stu_id} already exists')

class StudentNotFoundError(ProfileExceptions):
    def __init__(self):
        super().__init__(f'Student not found!')


class StudentIdFormatError(ProfileExceptions):
    def __init__(self):
        super().__init__("Please use correct id format (STU/00/00/0000)")

class IdYearError(ProfileExceptions):
    def __init__(self):
        super().__init__("Academic years in student_id must be consecutive e.g (STU/10/11/0000)")

class AdmissionDateError(ProfileExceptions):
    def __init__(self):
        super().__init__('Admission date cannot be in the future')

class ArchivedStudentNotFound(ProfileExceptions):
    def __init__(self):
        super().__init__("Student not found in archived records")

class NoArchiveRecords(ProfileExceptions):
    def __init__(self):
        super().__init__("No archived records")



