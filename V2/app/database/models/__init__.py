from .common_imports import Base

from .profiles import Students, Parents, Staff, Educator, Operations, Support, System
from .documents import StudentDocuments
from .auth_models import AccessLevelChanges
from .student_organization import StudentDepartments, Classes
from .staff_organization import StaffDepartments, StaffRoles, EducatorQualifications
from .academic import (Subjects, Grades, TotalGrades, StudentSubjects,
                     StudentDepartmentTransfers)

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
    "EducatorQualifications"
]