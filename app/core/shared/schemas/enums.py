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
    AWARD = 'AWARD'
    CERTIFICATE = 'CERTIFICATE'
    ARTICLE = 'ARTICLE'
    OTHER = 'OTHER'


class StaffType(str, Enum):
    EDUCATOR = 'Educator'
    ADMIN = 'Admin'
    SUPPORT = 'Support'
    SYSTEM = 'System'

class AccessLevel(str, Enum):
    INACTIVE = 'INACTIVE'
    READ = 'READ'
    EDUCATOR = 'EDUCATOR'
    ADMIN = 'ADMIN'
    SUPERUSER = 'SUPERUSER'
    SYSTEM = 'SYSTEM'

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
    PRACTICALS = 'PRACTICALS'
    MOCKEXAM = 'MOCKEXAM'
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
