from .common_imports import Base

from .profiles import Students, Parents, Staff, Educator, Operations, Support, System
from .documents import StudentDocuments
from .auth_models import AccessLevelChanges
from .staff_organization import StaffDepartments, StaffRoles, EducatorQualifications
from .student_organization import StudentDepartments, Classes, AcademicLevel, StudentDepartmentTransfers, StudentClassTransfer
from .academic import (Subjects, Grades, TotalGrades, StudentSubjects, AcademicLevelSubjects,SubjectEducators,StudentRepetitions)

__all__ = [
    "Base",
    "Students",
    "Parents",
    "Staff",
    "Educator",
    "Operations",
    "Support",
    "System",
    "StudentDocuments",
    "StaffDepartments",
    "StaffRoles",
    "StudentDepartments",
    "AccessLevelChanges",
    "Classes",
    "Subjects",
    "Grades",
    "TotalGrades",
    "StudentSubjects",
    "StudentDepartments",
    "StudentDepartmentTransfers",
    "StudentClassTransfer",
    "EducatorQualifications"
]