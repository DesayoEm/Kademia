from .common_imports import Base
from ....curriculum.models.curriculum import SubjectEducator, StudentSubject, Subject, AcademicLevelSubject
from ....transfer.models.transfer import StudentDepartmentTransfer, ClassTransfer
from ....documents.models.documents import StudentDocument, StudentAward
from ....auth.models.auth import AccessLevelChange
from ....staff_management.models.staff_management import StaffDepartment, StaffRole, EducatorQualification
from ....academic_structure.models.academic_structure import StudentDepartment, Classes, AcademicLevel
from ....transfer.models.transfer import StudentDepartmentTransfer, ClassTransfer
from ....assessment.models.assessment import Grade, TotalGrade,Repetition
from ....identity.models.staff import Staff, Educator, AdminStaff, SupportStaff, System
from ....identity.models.student import Student
from ....identity.models.guardian import Guardian


__all__ = [
    "Base",
    "Student",
    "Guardian",
    "Staff",
    "Educator",
    "AdminStaff",
    "SupportStaff",
    "System",
    "StudentDocument",
    "StaffDepartment",
    "StaffRole",
    "StudentDepartment",
    "AccessLevelChange",
    "Classes",
    "Subject",
    "Grade",
    "TotalGrade",
    "Repetition",
    "AcademicLevel",
    "AcademicLevelSubject",
    "StudentSubject",
    "SubjectEducator",
    "StudentDepartment",
    "StudentDepartmentTransfer",
    "ClassTransfer",
    "EducatorQualification",
    "StudentAward"
]