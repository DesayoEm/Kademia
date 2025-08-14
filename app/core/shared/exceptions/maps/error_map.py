"""error_map

Maps entity models to error metadata used in dynamic exception handling.
Format: ModelClass → (model_class, identity-facing display_name)

Used by service factories to:
- Raise EntityNotFoundError, ArchiveDependencyError, etc.
- Provide identity-facing names in error messages

REQUIRED for all models using dynamic exception logic
If missing, Kademia will crash while attempting to raise an exception.

Example:
    Student: (Student, "Student")
"""
from ....curriculum.models.curriculum import SubjectEducator, StudentSubject, Subject, AcademicLevelSubject
from ....documents.models.documents import StudentDocument, StudentAward
from ....rbac.models import RoleHistory
from app.core.staff_management.models import StaffDepartment, StaffTitle, EducatorQualification
from app.core.academic_structure.models import StudentDepartment, Classes, AcademicLevel
from ....transfer.models.transfer import DepartmentTransfer
from ....assessment.models.assessment import Grade, TotalGrade
from app.core.progression.models.progression import Repetition, Promotion
from ....identity.models.staff import Staff, Educator, AdminStaff, SupportStaff
from ....identity.models.student import Student
from ....identity.models.guardian import Guardian

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
    StaffTitle: (StaffTitle, "title"),
    StaffDepartment: (StaffDepartment, "department"),
    EducatorQualification: (EducatorQualification, "qualification"),

    # Student organization models
    AcademicLevel: (AcademicLevel, "academic level"),
    StudentDepartment: (StudentDepartment, "department"),
    Classes: (Classes, "class"),
    DepartmentTransfer: (DepartmentTransfer, "department transfer"),

    # Curriculum models
    Subject: (Subject, "subject"),
    AcademicLevelSubject: (AcademicLevelSubject, "curriculum assignment"),
    StudentSubject: (StudentSubject, "subject enrollment"),
    SubjectEducator: (SubjectEducator, "subject assignment"),
    Grade: (Grade, "grade"),
    TotalGrade: (TotalGrade, "total grade"),
    StudentAward: (StudentAward, "award"),

    # Document models
    StudentDocument: (StudentDocument, "document"),

    # Auth models
    RoleHistory: (RoleHistory, "role history"),

    # Progression
    Repetition: (Repetition, "repetition record"),
    Promotion: (Promotion, "promotion record")
}
