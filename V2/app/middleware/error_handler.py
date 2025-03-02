from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from ..services.errors.database_errors import *
from ..services.errors.staff_organisation_errors import *



class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            if isinstance(e, EntityNotFoundError):
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"detail": e.user_message}
                )
            elif isinstance(e, UniqueViolationError):
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content={"detail": e.user_message}
                )
            elif isinstance(e, RelationshipError):
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": e.user_message}
                )
            elif isinstance(e, DatabaseError):
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"detail": e.user_message}
                )
            elif (isinstance(e, DepartmentNotFoundError) or
                  isinstance(e, RoleNotFoundError) or
                  isinstance(e, QualificationNotFoundError)):

                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"detail": e.user_message}
                )
            elif (isinstance(e, DuplicateDepartmentError) or
                        isinstance(e, DuplicateRoleError) or
                        isinstance(e, DuplicateDepartmentError)):
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": e.user_message}
                )
            elif isinstance(e, DuplicateQualificationError):
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": e.user_message}
                )
            elif isinstance(e, EmptyFieldError):
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": e.user_message}
                )
            elif isinstance(e, BlankFieldError):
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": e.user_message}
                )
            elif isinstance(e, TextTooShortError):
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": e.user_message}
                )

            # For unhandled exceptions
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "An unexpected error occurred"}
            )