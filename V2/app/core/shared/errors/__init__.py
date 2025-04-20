import sys
import inspect
import pkgutil
import logging


from .base_error import KademiaError

from .archive_delete_errors import (
    ArchiveAndDeleteError,
    CascadeDeletionError,
    ArchiveDependencyError,
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
    RelatedEntityNotFoundError,
    UniqueViolationError,
    DuplicateEntityError,
    EntityInUseError,
    RelationshipError,
    TransactionError,
    DBConnectionError,
    DatabaseError,
    NullFKConstraintMisconfiguredError,
    CascadeFKConstraintMisconfiguredError,
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
    TextTooShortError,
    DBTextTooLongError,
    TextTooLongError,
    FutureDateError,
    DateFormatError,
    PastDateError,
    InvalidYearError,
    InvalidYearLengthError,
    InvalidOrderNumberError,
    InvalidCharacterError,
    InvalidPhoneError,
    EmailFormatError,
)

from .staff_organisation_errors import (
    StaffOrganizationError,
    LifetimeValidityConflictError,
    TemporaryValidityConflictError,
)

from .student_organisation_errors import (
    StudentOrganizationError,
    InvalidCodeError,
)

from .user_errors import (
    IdentityError,
    StaffTypeError,
    DuplicateStudentIDError,
    InvalidSessionYearError
)

logging.basicConfig(level=logging.INFO)

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __import__(f"{__name__}.{module_name}", fromlist=["*"])

current_module = sys.modules[__name__]

__all__ = [
    name for name, obj in inspect.getmembers(current_module)
    if inspect.isclass(obj) and issubclass(obj, KademiaError) and obj is not KademiaError
]