from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid
from ..core.errors.database_errors import *
from ..core.errors.export_errors import UnimplementedGathererError
from ..core.errors.staff_organisation_errors import *
from ..core.errors.input_validation_errors import *
from ..core.errors.student_organisation_errors import *
from ..core.errors.user_errors import *
from ..core.errors.auth_errors import *
from ..core.errors.email_errors import *
from ..log_service.logger import logger

class ExceptionMiddleware(BaseHTTPMiddleware):

    error_map = {

        # Email errors
        EmailFailedToSendError: status.HTTP_500_INTERNAL_SERVER_ERROR,

        # Auth errors
        InvalidCredentialsError: status.HTTP_401_UNAUTHORIZED,
        WrongPasswordError: status.HTTP_401_UNAUTHORIZED,
        PasswordFormatError: status.HTTP_400_BAD_REQUEST,
        UserNotFoundError: status.HTTP_404_NOT_FOUND,

        TokenError: status.HTTP_401_UNAUTHORIZED,
        TokenExpiredError: status.HTTP_401_UNAUTHORIZED,
        TokenInvalidError: status.HTTP_401_UNAUTHORIZED,
        ResetLinkExpiredError: status.HTTP_401_UNAUTHORIZED,
        AccessTokenRequiredError: status.HTTP_401_UNAUTHORIZED,
        RefreshTokenRequiredError: status.HTTP_401_UNAUTHORIZED,
        TokenRevokedError: status.HTTP_401_UNAUTHORIZED,

        # Generic database errors
        DatabaseError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        EntityNotFoundError: status.HTTP_404_NOT_FOUND,
        UniqueViolationError: status.HTTP_409_CONFLICT,
        RelationshipError: status.HTTP_400_BAD_REQUEST,
        TransactionError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        DBConnectionError: status.HTTP_500_INTERNAL_SERVER_ERROR,

        # Generic input validation errors
        EmptyFieldError: status.HTTP_400_BAD_REQUEST,
        BlankFieldError: status.HTTP_400_BAD_REQUEST,
        TextTooShortError: status.HTTP_400_BAD_REQUEST,
        InvalidCharacterError: status.HTTP_400_BAD_REQUEST,
        InvalidCodeError: status.HTTP_400_BAD_REQUEST,
        InvalidPhoneError: status.HTTP_400_BAD_REQUEST,
        EmailFormatError: status.HTTP_400_BAD_REQUEST,
        DateError: status.HTTP_400_BAD_REQUEST,
        DateFormatError: status.HTTP_400_BAD_REQUEST,
        PastDateError: status.HTTP_400_BAD_REQUEST,
        InvalidValidityYearError: status.HTTP_400_BAD_REQUEST,
        InvalidYearError: status.HTTP_400_BAD_REQUEST,
        InvalidYearLengthError: status.HTTP_400_BAD_REQUEST,
        InvalidSessionYearError: status.HTTP_400_BAD_REQUEST,
        InvalidOrderNumberError: status.HTTP_400_BAD_REQUEST,
        TextTooLongError: status.HTTP_400_BAD_REQUEST,
        DBTextTooLongError: status.HTTP_400_BAD_REQUEST,

        # Staff organization errors
        DepartmentNotFoundError: status.HTTP_404_NOT_FOUND,
        DuplicateDepartmentError: status.HTTP_409_CONFLICT,
        RelatedDepartmentNotFoundError: status.HTTP_404_NOT_FOUND,

        RoleNotFoundError: status.HTTP_404_NOT_FOUND,
        RelatedRoleNotFoundError: status.HTTP_404_NOT_FOUND,
        DuplicateRoleError: status.HTTP_409_CONFLICT,
        RoleArchivalDependencyError: status.HTTP_409_CONFLICT,
        RoleDeletionDependencyError: status.HTTP_409_CONFLICT,

        QualificationNotFoundError: status.HTTP_404_NOT_FOUND,
        DuplicateQualificationError: status.HTTP_409_CONFLICT,
        LifetimeValidityConflictError: status.HTTP_400_BAD_REQUEST,
        TemporaryValidityConflictError: status.HTTP_400_BAD_REQUEST,

        # Student organization errors
        ClassNotFoundError: status.HTTP_404_NOT_FOUND,
        DuplicateClassError: status.HTTP_409_CONFLICT,

        LevelNotFoundError: status.HTTP_404_NOT_FOUND,
        RelatedLevelNotFoundError: status.HTTP_404_NOT_FOUND,
        DuplicateLevelError: status.HTTP_409_CONFLICT,

        StudentDepartmentNotFoundError: status.HTTP_404_NOT_FOUND,
        RelatedStudentDepartmentNotFoundError: status.HTTP_404_NOT_FOUND,
        DuplicateStudentDepartmentError: status.HTTP_409_CONFLICT,

        # User profile errors (Staff/Student/Guardian)
        StaffTypeError: status.HTTP_400_BAD_REQUEST,
        StaffNotFoundError: status.HTTP_404_NOT_FOUND,
        DuplicateStaffError: status.HTTP_409_CONFLICT,
        RelatedStaffNotFoundError: status.HTTP_404_NOT_FOUND,
        RelatedEducatorNotFoundError: status.HTTP_404_NOT_FOUND,

        StudentNotFoundError: status.HTTP_404_NOT_FOUND,
        RelatedStudentNotFoundError: status.HTTP_404_NOT_FOUND,
        DuplicateStudentError: status.HTTP_409_CONFLICT,
        DuplicateStudentIDError: status.HTTP_409_CONFLICT,

        GuardianNotFoundError: status.HTTP_404_NOT_FOUND,
        RelatedGuardianNotFoundError: status.HTTP_404_NOT_FOUND,
        DuplicateGuardianError: status.HTTP_409_CONFLICT,

        # Export errors
        UnimplementedGathererError: status.HTTP_500_INTERNAL_SERVER_ERROR,

    }


    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        logger.info(f"Request started | {request_id} | {request.method} {request.url.path}")
        start_time = time.time()

        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            logger.info(f"Request completed | {request_id} | Status: {response.status_code} | Time: {process_time:.3f}s")
            return response

        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"Unhandled exception | {request_id} | {str(e)}", exc_info=True)
            return self.handle_exception(e, request_id)

    def create_json_response(self, e, status_code):
        return JSONResponse(
            status_code=status_code,
            content={"detail": e.user_message}
        )

    def handle_exception(self, e, request_id):
        if isinstance(e, HTTPException):
            logger.warning(f"HTTPException | {request_id} | {e.detail}")
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )

        for error, status_code in self.error_map.items():
            if isinstance(e, error):
                log_level = logger.warning if status_code < 500 else logger.error
                log_level(f"{error.__name__} | {request_id} | {e.log_message}")
                return self.create_json_response(e, status_code)

        log_message = f"Unhandled exception | {request_id} | {str(e)}"

       #Uncaught errors
        logger.error(log_message, exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An unexpected error occurred.",
            }
        )
