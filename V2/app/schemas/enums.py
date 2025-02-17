from enum import Enum

class ArchiveReason(str, Enum):
    ERROR = 'ERROR'
    GRADUATED = 'GRADUATED'
    TRANSFERRED = 'TRANSFERRED'
    WITHDRAWN = 'WITHDRAWN'
    ADMINISTRATIVE = 'ADMINISTRATIVE'


class ClassCode(str, Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'

class ApprovalStatus (str, Enum):
    PENDING = 'Pending'
    APPROVED= 'Approved'
    REJECTED = 'Rejected'

class GradeType (str, Enum):
    EXAM = 'Exam'
    TEST = 'Test'
    ASSIGNMENT = 'Assignment'
    PRACTICALS = 'Practicals'
    MOCKEXAM = 'Mock exam'
    EXTRACURRICULLAR = 'Extracurricular'


class Term (str, Enum):
    FIRST = 'First'
    SECOND = 'Second'
    THIRD = 'Third'


class Gender(str, Enum):
    MALE = 'M'
    FEMALE = 'F'

class StaffType(str, Enum):
    STAFF = "staff"
    EDUCATOR = "educator"
    ADMINISTRATOR = "admin"
    SUPPORT = "support"

class DocumentType(str, Enum):
    RESULT = "result"
    ID = "id"
    AWARD = "award"
    CERTIFICATE = "certificate"
    ARTICLE = "article"
    OTHER = "other"

class DepartmentName(str, Enum):
    SCIENCE = 'science'
    HUMANITIES = 'humanities'
    BUSINESS = 'business'



class SubjectGroup(str, Enum):
    SCIENCE = 'science'
    HUMANITIES = 'humanities'
    BUSINESS = 'business'
    General = 'General'


class UserType (str, Enum):
    STUDENT = 'Student'
    PARENT = 'Parent'
    ADMIN = 'Admin'
    EDUCATOR = 'Educator'


class AccessLevel (str, Enum):
    USER = 'User'
    ADMIN = 'Admin'
    SUPERUSER = 'Superuser'
