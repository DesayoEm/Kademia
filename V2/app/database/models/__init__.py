from .common_imports import Base

from .users import Student, Guardian, Staff, Educator, AdminStaff, SupportStaff, System
from .documents import StudentDocument
from .auth_models import AccessLevelChange
from .staff_organization import StaffDepartment, StaffRole, EducatorQualification
from .student_organization import StudentDepartment, Classes, AcademicLevel, StudentDepartmentTransfer, ClassTransfer
from .academic import (Subject, Grade, TotalGrade, StudentSubject, AcademicLevelSubject,SubjectEducator,Repetition,
                       StudentAward)

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
    "StudentDepartment",
    "StudentDepartmentTransfer",
    "ClassTransfer",
    "EducatorQualification",
    "StudentAward"
]