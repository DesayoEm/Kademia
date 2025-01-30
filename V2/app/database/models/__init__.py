from .common_imports import Base

from .profiles import Students, Parents, Staff, Educator, Operations, Support, System
from .documents import StudentDocuments
from .organization import StaffDepartments, StaffRoles, Departments, Classes
from .academic import (Subjects, Grades, TotalGrades, StudentSubjects,
                       Repetitions, StudentTransfers, EducatorQualifications)

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
    "Departments",
    "Classes",
    "Subjects",
    "Grades",
    "TotalGrades",
    "StudentSubjects",
    "Repetitions",
    "StudentTransfers"
]