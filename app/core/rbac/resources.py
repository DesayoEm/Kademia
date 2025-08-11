from enum import Enum

class Resource(Enum):
    ACCESS_LEVEL_CHANGE = "access_level_change"

    STUDENTS = "students"
    STAFF = "staff"
    EDUCATORS = "educators"
    GUARDIANS = "guardians"

    STAFF_DEPARTMENTS = "staff_departments"
    STAFF_ROLES = "staff_roles"
    EDUCATOR_QUALIFICATIONS = "educator_qualifications"

    CLASSES = "classes"
    DEPARTMENTS = "departments"
    ACADEMIC_LEVELS = "academic_levels"

    SUBJECTS = "subjects"
    ACADEMIC_LEVEL_SUBJECTS = "academic_level_subjects"
    STUDENT_SUBJECTS = "student_subjects"
    SUBJECT_EDUCATORS = "subject_educators"

    GRADES = "grades"
    TOTAL_GRADES = "total_grades"

    DOCUMENTS = "documents"
    AWARDS = "awards"

    TRANSFERS = "transfers"
    PROMOTIONS = "promotions"
    REPETITIONS = "repetitions"

    AUDITS = "audits"
    SYSTEM_CONFIG = "system_config"