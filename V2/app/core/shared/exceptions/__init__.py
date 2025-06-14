import sys
import inspect
import pkgutil
import logging


from .base_error import KademiaError

from .lifecycle_errors import (
    ArchiveAndDeleteError,
    CascadeDeletionError,
    ArchiveDependencyError,
)

from .auth_errors import (
    AuthError,
    CurrentPasswordError,
    InvalidPasswordTokenError,
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
    SameLevelError
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
    KDDatabaseError,
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
    EntryValidationError,
    FileTooSmallError,
    FileTooLargeError,
    UnsupportedFileFormatError,
    EmptyFileError,
    EmptyFieldError,
    TextTooShortError,
    DBTextTooLongError,
    TextTooLongError,
    SessionYearFormatError,
    InvalidSessionRangeError,
    SessionYearFormatError,
    InvalidYearError,
    InvalidYearLengthError,
    FutureDateError,
    FutureYearError,
    PastYearError,
    DateFormatError,
    PastDateError,
    InvalidYearError,
    InvalidYearLengthError,
    InvalidOrderNumberError,
    InvalidCharacterError,
    InvalidPhoneError,
    EmailFormatError,
)

from .staff_management_errors import (
    StaffOrganizationError,
    LifetimeValidityConflictError,
    TemporaryValidityConflictError,
)

from .academic_structure_errors import (
    StudentOrganizationError,
    InvalidCodeError,
    InvalidRankNumberError,
    InvalidOrderNumberError
)

from .identity_errors import (
    IdentityError,
    StaffTypeError,
    DuplicateStudentIDError,
    InvalidSessionYearError
)
from .assessment_errors import (
    ScoreExceedsMaxError,
    MaxScoreTooHighError,
    InvalidWeightError
)

from .progression_errors import (
    InvalidRepetitionLevelError,
    InvalidPromotionLevelError
)

logging.basicConfig(level=logging.INFO)

for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __import__(f"{__name__}.{module_name}", fromlist=["*"])

current_module = sys.modules[__name__]

__all__ = [
    name for name, obj in inspect.getmembers(current_module)
    if inspect.isclass(obj) and issubclass(obj, KademiaError) and obj is not KademiaError
]