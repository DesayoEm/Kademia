from enum import Enum

class Gender(str, Enum):
    MALE = 'M'
    FEMALE = 'F'

class StaffType(str, Enum):
    EDUCATOR = "educator"
    ADMINISTRATOR = "admin"
    SUPPORT = "support"

class DocumentType(str, Enum):
    RESULT = "Result"
    ID = "id"
    AWARD = "Award"
    CERTIFICATE = "Certificate"
    ARTICLE = "Article"
    OTHER = "Other"


class DepartmentName(str, Enum):
    SCIENCE = 'Science'
    HUMANITIES = 'Humanities'
    BUSINESS = 'Business'


class DepartmentCode(str, Enum):
    SCI = 'SCI'
    HMS= 'HMS'
    BSN = 'BSN'


class ClassLevel(str, Enum):
    JuniorSecondarySchool1 = 'JSS 1'
    JuniorSecondarySchool2 = 'JSS 2'
    JuniorSecondarySchool3 = 'JSS 3'
    SeniorSecondarySchool1 = 'SSS 1'
    SeniorSecondarySchool2 = 'SSS 2'
    SeniorSecondarySchool3 = 'SSS 3'
    ALevels = 'A Levels'


class ClassCode(str, Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'


class Term (str, Enum):
    FIRST = 'First'
    SECOND = 'Second'
    THIRD = 'Third'


class SubjectGroup(str, Enum):
    SCIENCE = 'Science'
    HUMANITIES = 'Humanities'
    BUSINESS = 'Business'
    GENERAL = 'General'



class GradeType (str, Enum):
    EXAM = 'Exam'
    TEST = 'Test'
    ASSIGNMENT = 'Assignment'
    PRACTICALS = 'Practicals'
    MOCKEXAM = 'Mock exam'
    EXTRACURRICULLAR = 'Extracurricular'


class UserType (str, Enum):
    STUDENT = 'Student'
    PARENT = 'Parent'
    ADMIN = 'Admin'
    EDUCATOR = 'Educator'


class ApprovalStatus (str, Enum):
    PENDING = 'Pending'
    APPROVED= 'Approved'
    REJECTED = 'Rejected'


class StaffDepartmentName (str, Enum):
    ADMIN = 'Admin'
    EDUCATION = 'Education'
    OPERATIONS = 'Operations'
    SUPPORT = 'Support'
    OTHER = 'Other'


class AccessLevel (str, Enum):
    USER = 'User'
    ADMIN = 'Admin'
    SUPERUSER = 'Superuser'
    SUPERADMIN = 'Superadmin'
