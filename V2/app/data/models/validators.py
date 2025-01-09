from enum import Enum

class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'

class StaffType(str, Enum):
    STAFF = "staff"
    EDUCATOR = "educator"
    ADMINISTRATOR = "admin"
    SUPPORT = "support"

class DocumentType(str, Enum):
    RESULT = "result"
    AWARD = "award"
    CERTIFICATE = "certificate"
    ARTICLE = "article"
    OTHER = "other"

class DepartmentType(str, Enum):
    SCIENCE = 'science'
    HUMANITIES = 'humanities'
    BUSINESS = 'business'

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

class StaffDepartmentName (str, Enum):
    ADMIN = 'Admin'
    EDUCATION = 'Education'
    MANAGEMENT = 'Management'
    OTHER = 'Other'


class Term (str, Enum):
    FIRST = 'First'
    SECOND = 'Second'
    THIRD = 'Third'


class GradeType (str, Enum):
    EXAM = 'Exam'
    TEST = 'Test'
    THIRD = 'Assignment'
    PRACTICAL = 'Practical'
    MOCKEXAM = 'Mock exam'

class UserType (str, Enum):
    STUDENT = 'Student'
    PARENT = 'Parent'
    ADMIN = 'Admin'
    EDUCATOR = 'Educator'

