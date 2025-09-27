from enum import Enum

class Gender(str, Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    SYSTEM = 'SYSTEM'

class Title(str, Enum):
    Ms = 'Ms'
    Mrs = 'Mrs'
    Mr = 'Mr'

class ValidityType(str, Enum):
    Temporary = 'Temporary'
    Lifetime = 'Lifetime'

class UserType(str, Enum):
    STUDENT = 'STUDENT'
    GUARDIAN = 'GUARDIAN'
    STAFF = 'STAFF'
    SYSTEM = 'SYSTEM'


class DocumentType(str, Enum):
    RESULT = 'RESULT'
    ID = 'ID'
    CERTIFICATE = 'CERTIFICATE'
    ARTICLE = 'ARTICLE'
    OTHER = 'OTHER'


class StaffType(str, Enum):
    EDUCATOR = 'Educator'
    ADMIN = 'Admin'
    SUPPORT = 'Support'
    SYSTEM = 'System'


class StaffAvailability(str, Enum):
    AVAILABLE = 'AVAILABLE'
    UNAVAILABLE = 'UNAVAILABLE'


class EmploymentStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    LEFT = 'LEFT'


class StudentStatus(str, Enum):
    ENROLLED = 'ENROLLED'
    LEFT = 'LEFT'
    GRADUATED = 'GRADUATED'


class ClassCode(str, Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'


class Term(str, Enum):
    FIRST = 'FIRST'
    SECOND = 'SECOND'
    THIRD = 'THIRD'


class SubjectGroup(str, Enum):
    SCIENCE = 'SCIENCE'
    HUMANITIES = 'HUMANITIES'
    BUSINESS = 'BUSINESS'
    GENERAL = 'GENERAL'


class GradeType(str, Enum):
    EXAM = 'EXAM'
    TEST = 'TEST'
    ASSIGNMENT = 'ASSIGNMENT'
    PRACTICAL = 'PRACTICAL'
    MOCK = 'MOCK'
    EXTRACURRICULAR = 'EXTRACURRICULAR'


class ApprovalStatus(str, Enum):
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


class ArchiveReason(str, Enum):
    ERROR = 'ERROR'
    GRADUATED = 'GRADUATED'
    TRANSFERRED = 'TRANSFERRED'
    WITHDRAWN = 'WITHDRAWN'
    ADMINISTRATIVE = 'ADMINISTRATIVE'


class ExportFormat(str, Enum):
    pdf = "pdf"
    csv = "csv"
    excel = "excel"


class UserRoleName(str, Enum):
    INACTIVE = 'INACTIVE'
    STUDENT = 'STUDENT'
    GUARDIAN = 'GUARDIAN'
    EDUCATOR = 'EDUCATOR'
    SUPER_EDUCATOR = 'SUPER_EDUCATOR'
    ADMIN = 'ADMIN'
    SUPERUSER = 'SUPERUSER'
    SYSTEM = 'SYSTEM'


class Action(Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    ARCHIVE = "ARCHIVE"
    RESTORE = "RESTORE"
    APPROVE = "APPROVE"
    REJECT = "REJECT"


class Resource(Enum):
    ROLE = "ROLE"
    ROLE_CHANGE = "ROLE_CHANGE"
    ROLE_PERMISSION = "ROLE_PERMISSION"


    STUDENT = "STUDENT"
    STAFF = "STAFF"
    EDUCATOR = "EDUCATOR"
    GUARDIAN = "GUARDIAN"

    STAFF_DEPARTMENT = "STAFF_DEPARTMENT"
    STAFF_JOB_TITLE = "STAFF_JOB_TITLE"
    EDUCATOR_QUALIFICATION = "EDUCATOR_QUALIFICATION"

    CLASSES = "CLASSES"
    DEPARTMENT = "DEPARTMENT"
    ACADEMIC_LEVEL = "ACADEMIC_LEVEL"

    SUBJECT = "SUBJECT"
    ACADEMIC_LEVEL_SUBJECT = "ACADEMIC_LEVEL_SUBJECT"
    STUDENT_SUBJECT = "STUDENT_SUBJECT"
    SUBJECT_EDUCATOR = "SUBJECT_EDUCATOR"

    GRADE = "GRADE"
    TOTAL_GRADE = "TOTAL_GRADE"

    DOCUMENT = "DOCUMENT"
    AWARD = "AWARD"

    TRANSFER = "TRANSFER"
    PROMOTION = "PROMOTION"
    REPETITION = "REPETITION"

    AUDIT = "AUDIT"
    SYSTEM_CONFIG = "SYSTEM_CONFIG"