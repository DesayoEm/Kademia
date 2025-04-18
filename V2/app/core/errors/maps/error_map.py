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

# Entity: entity_model, display_name
error_map = {
    StaffRole: (StaffRole, "role"),
    StaffDepartment: (StaffDepartment, "department"),
    EducatorQualification: (EducatorQualification, "qualification"),

    AcademicLevel: (AcademicLevel, "level"),
    StudentDepartment: (StudentDepartment, "department"),
    Classes: (Classes, "class")


        }
