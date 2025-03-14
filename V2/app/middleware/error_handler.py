from fastapi import Request, status, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid
from ..services.errors.database_errors import *
from ..services.errors.staff_organisation_errors import *
from ..services.errors.student_organisation_errors import *
from ..logging.logger import logger

class ExceptionMiddleware(BaseHTTPMiddleware):

    error_map = {
        EntityNotFoundError: status.HTTP_404_NOT_FOUND,
        DepartmentNotFoundError: status.HTTP_404_NOT_FOUND,
        LevelNotFoundError: status.HTTP_404_NOT_FOUND,
        DuplicateLevelError: status.HTTP_409_CONFLICT,
        RoleNotFoundError: status.HTTP_404_NOT_FOUND,
        QualificationNotFoundError: status.HTTP_404_NOT_FOUND,
        UniqueViolationError: status.HTTP_409_CONFLICT,
        DuplicateDepartmentError: status.HTTP_409_CONFLICT,
        DuplicateRoleError: status.HTTP_409_CONFLICT,
        DuplicateQualificationError: status.HTTP_409_CONFLICT,
        RelationshipError: status.HTTP_400_BAD_REQUEST,
        EmptyFieldError: status.HTTP_400_BAD_REQUEST,
        BlankFieldError: status.HTTP_400_BAD_REQUEST,
        TextTooShortError: status.HTTP_400_BAD_REQUEST,
        DatabaseError: status.HTTP_500_INTERNAL_SERVER_ERROR
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

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred"}
        )
