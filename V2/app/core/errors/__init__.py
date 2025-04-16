# __init__.py

# Standard library imports
import sys
import inspect
import pkgutil
import logging

# Explicit imports so editor knows about the classes
from .base_error import KademiaError

from .archive_delete_errors import (
    ArchiveAndDeleteError,
    CascadeDeletionError,
    DeletionDependencyError,
)

from .auth_errors import (
    AuthError,
    InvalidCredentialsError,
    WrongPasswordError,
    PasswordFormatError,
    UserNotFoundError,
    TokenError,
    TokenExpiredError,
    ResetLinkExpiredError,
    TokenInvalidError,
    AccessTokenRequiredError,
    RefreshTokenRequiredError,
    TokenRevokedError,
)

from .database_errors import (
    DBError,
    EntityNotFoundError,
    UniqueViolationError,
    RelationshipError,
    TransactionError,
    DBConnectionError,
    DatabaseError,
)

from .email_errors import (
    EmailError,
    EmailFailedToSendError,
)

from .export_errors import (
    ExportError,
    ExportFormatError,
    UnimplementedGathererError,
)

from .entry_validation_errors import (
    InputValidationError,
    EmptyFieldError,
    BlankFieldError,
    TextTooShortError,
    DBTextTooLongError,
    TextTooLongError,
    DateError,
    DateFormatError,
    PastDateError,
    InvalidValidityYearError,
    InvalidYearError,
    InvalidYearLengthError,
    InvalidSessionYearError,
    InvalidCodeError,
    InvalidOrderNumberError,
    InvalidCharacterError,
    InvalidPhoneError,
    EmailFormatError,
)

from .staff_organisation_errors import (
    StaffOrganizationError,
    DuplicateDepartmentError,
    DepartmentInUseError,
    DepartmentNotFoundError,
    RelatedDepartmentNotFoundError,
    DuplicateRoleError,
    RoleNotFoundError,
    RelatedRoleNotFoundError,
    RoleArchivalDependencyError,
    RoleDeletionDependencyError,
    DuplicateQualificationError,
    QualificationNotFoundError,
    QualificationInUseError,
    LifetimeValidityConflictError,
    TemporaryValidityConflictError,
)

from .student_organisation_errors import (
    StudentOrganizationError,
    DuplicateStudentDepartmentError,
    StudentDepartmentNotFoundError,
    RelatedStudentDepartmentNotFoundError,
    StudentDepartmentInUseError,
    DuplicateLevelError,
    LevelNotFoundError,
    RelatedLevelNotFoundError,
    LevelInUseError,
    DuplicateClassError,
    ClassNotFoundError,
    RelatedClassNotFoundError,
    ClassInUseError,
)

from .user_errors import (
    UserProfileError,
    DuplicateStaffError,
    StaffNotFoundError,
    RelatedStaffNotFoundError,
    RelatedEducatorNotFoundError,
    StaffInUseError,
    StaffTypeError,
    DuplicateStudentIDError,
    DuplicateStudentError,
    StudentNotFoundError,
    RelatedStudentNotFoundError,
    StudentInUseError,
    RelatedGuardianNotFoundError,
    DuplicateGuardianError,
    GuardianNotFoundError,
)

logging.basicConfig(level=logging.INFO)

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __import__(f"{__name__}.{module_name}", fromlist=["*"])

current_module = sys.modules[__name__]

__all__ = [
    name for name, obj in inspect.getmembers(current_module)
    if inspect.isclass(obj) and issubclass(obj, KademiaError) and obj is not KademiaError
]
