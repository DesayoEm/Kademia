from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid

from app.core.shared.exceptions import *
from app.infra.log_service.logger import logger, auth_logger


class ExceptionMiddleware(BaseHTTPMiddleware):

    error_map = {

        # Email exceptions
        EmailFailedToSendError: status.HTTP_500_INTERNAL_SERVER_ERROR,

        # Auth exceptions
        AuthError: status.HTTP_401_UNAUTHORIZED,
        InvalidPasswordTokenError: status.HTTP_401_UNAUTHORIZED,
        InvalidCredentialsError: status.HTTP_401_UNAUTHORIZED,
        WrongPasswordError: status.HTTP_401_UNAUTHORIZED,
        PasswordFormatError: status.HTTP_400_BAD_REQUEST,
        UserNotFoundError: status.HTTP_404_NOT_FOUND,
        SameLevelError: status.HTTP_400_BAD_REQUEST,
        CurrentPasswordError: status.HTTP_400_BAD_REQUEST,

        TokenError: status.HTTP_401_UNAUTHORIZED,
        TokenExpiredError: status.HTTP_401_UNAUTHORIZED,
        TokenInvalidError: status.HTTP_401_UNAUTHORIZED,
        ResetLinkExpiredError: status.HTTP_401_UNAUTHORIZED,
        AccessTokenRequiredError: status.HTTP_401_UNAUTHORIZED,
        RefreshTokenRequiredError: status.HTTP_401_UNAUTHORIZED,
        TokenRevokedError: status.HTTP_401_UNAUTHORIZED,

        # Generic db exceptions
        KDDatabaseError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        EntityNotFoundError: status.HTTP_404_NOT_FOUND,
        RelatedEntityNotFoundError: status.HTTP_404_NOT_FOUND,
        UniqueViolationError: status.HTTP_409_CONFLICT,
        DuplicateEntityError: status.HTTP_409_CONFLICT,
        EntityInUseError: status.HTTP_409_CONFLICT,
        RelationshipError: status.HTTP_400_BAD_REQUEST,
        TransactionError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        DBConnectionError: status.HTTP_500_INTERNAL_SERVER_ERROR,

        #File errors
        FileTooSmallError: status.HTTP_400_BAD_REQUEST,
        FileTooLargeError: status.HTTP_400_BAD_REQUEST,
        EmptyFileError: status.HTTP_400_BAD_REQUEST,
        UnsupportedFileFormatError: status.HTTP_400_BAD_REQUEST,
        AbsentKeyError: status.HTTP_400_BAD_REQUEST,


        # Generic input validation exceptions
        EmptyFieldError: status.HTTP_400_BAD_REQUEST,
        SessionYearFormatError: status.HTTP_400_BAD_REQUEST,
        PastYearError: status.HTTP_400_BAD_REQUEST,
        FutureYearError: status.HTTP_400_BAD_REQUEST,
        InvalidSessionRangeError: status.HTTP_400_BAD_REQUEST,
        TextTooShortError: status.HTTP_400_BAD_REQUEST,
        TextTooLongError: status.HTTP_400_BAD_REQUEST,
        DBTextTooLongError: status.HTTP_400_BAD_REQUEST,
        InvalidCharacterError: status.HTTP_400_BAD_REQUEST,
        InvalidPhoneError: status.HTTP_400_BAD_REQUEST,
        EmailFormatError: status.HTTP_400_BAD_REQUEST,
        PastDateError: status.HTTP_400_BAD_REQUEST,
        FutureDateError: status.HTTP_400_BAD_REQUEST,
        DateFormatError: status.HTTP_400_BAD_REQUEST,
        InvalidYearError: status.HTTP_400_BAD_REQUEST,
        InvalidYearLengthError: status.HTTP_400_BAD_REQUEST,
        InvalidOrderNumberError: status.HTTP_400_BAD_REQUEST,


        # Staff management exceptions
        LifetimeValidityConflictError: status.HTTP_400_BAD_REQUEST,
        TemporaryValidityConflictError: status.HTTP_400_BAD_REQUEST,

        # Academic structure exceptions
        InvalidCodeError: status.HTTP_400_BAD_REQUEST,
        InvalidRankNumberError: status.HTTP_400_BAD_REQUEST,
        ClassLevelMismatchError: status.HTTP_400_BAD_REQUEST,


        # Curriculum exceptions
        AcademicLevelMismatchError: status.HTTP_400_BAD_REQUEST,


        # Assessment exceptions
        ScoreExceedsMaxError: status.HTTP_400_BAD_REQUEST,
        MaxScoreTooHighError: status.HTTP_400_BAD_REQUEST,
        WeightTooHighError:status.HTTP_400_BAD_REQUEST,
        InvalidWeightError:status.HTTP_400_BAD_REQUEST,
        FileAlreadyExistsError: status.HTTP_400_BAD_REQUEST,
        UnableToRecalculateError: status.HTTP_500_INTERNAL_SERVER_ERROR,

        # Progression exceptions
        InvalidPromotionLevelError: status.HTTP_400_BAD_REQUEST,
        InvalidRepetitionLevelError: status.HTTP_400_BAD_REQUEST,
        ProgressionStatusAlreadySetError: status.HTTP_400_BAD_REQUEST,
        LevelNotFinalError: status.HTTP_400_BAD_REQUEST,

        # User profile exceptions (Staff/Student/Guardian)
        StaffTypeError: status.HTTP_400_BAD_REQUEST,
        InvalidSessionYearError: status.HTTP_400_BAD_REQUEST,
        DuplicateStudentIDError: status.HTTP_409_CONFLICT,

        # Export exceptions
        UnimplementedGathererError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        ExportFormatError: status.HTTP_400_BAD_REQUEST,

        # Archive/delete exceptions
        CascadeDeletionError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        ArchiveDependencyError: status.HTTP_409_CONFLICT,

        # Transfer exceptions
        TransferStatusAlreadySetError: status.HTTP_400_BAD_REQUEST,

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

            if isinstance(e, AuthError) and hasattr(e, "user_message") and hasattr(e, "log_message"):
                auth_logger.warning(f"AuthError | {request_id} | {e.log_message}")
                return self.create_json_response(e, status.HTTP_403_FORBIDDEN)

        log_message = f"Unhandled exception | {request_id} | {str(e)}"


       #Uncaught exceptions
        logger.error(log_message, exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An unexpected error occurred.",
            }
        )

    @staticmethod
    def create_json_response(e, status_code):
        return JSONResponse(
            status_code=status_code,
            content={"detail": e.user_message}
        )
