"""error_map

Maps entity models to error metadata used in dynamic exception handling.
Format: ModelClass → (model_class, user-facing display_name)

Used by service factories to:
- Raise EntityNotFoundError, ArchiveDependencyError, etc.
- Provide user-facing names in error messages

REQUIRED for all models using dynamic exception logic
If missing, Kademia will crash while attempting to raise an exception.

Example:
    Student: (Student, "Student")
"""

from V2.app.database.models import *
from V2.app.core.errors import *

# Entity: (entity_model, display_name)
error_map = {
    # User models
    Guardian: (Guardian, "guardian"),
    Student: (Student, "student"),
    Staff: (Staff, "staff member"),
    Educator: (Educator, "educator"),
    AdminStaff: (AdminStaff, "administrative staff"),
    SupportStaff: (SupportStaff, "support staff"),

    # Staff organization models
    StaffRole: (StaffRole, "role"),
    StaffDepartment: (StaffDepartment, "department"),
    EducatorQualification: (EducatorQualification, "qualification"),

    # Student organization models
    AcademicLevel: (AcademicLevel, "academic level"),
    StudentDepartment: (StudentDepartment, "department"),
    Classes: (Classes, "class"),
    ClassTransfer: (ClassTransfer, "class transfer"),
    StudentDepartmentTransfer: (StudentDepartmentTransfer, "department transfer"),

    # Academic models
    Subject: (Subject, "subject"),
    AcademicLevelSubject: (AcademicLevelSubject, "curriculum assignment"),
    StudentSubject: (StudentSubject, "subject enrollment"),
    SubjectEducator: (SubjectEducator, "subject assignment"),
    Grade: (Grade, "grade"),
    TotalGrade: (TotalGrade, "total grade"),
    Repetition: (Repetition, "class repetition"),
    StudentAward: (StudentAward, "award"),

    # Document models
    StudentDocument: (StudentDocument, "document"),

    # Auth models
    AccessLevelChange: (AccessLevelChange, "access level change")
}
