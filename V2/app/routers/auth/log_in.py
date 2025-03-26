from sqlalchemy.orm import Session
from datetime import datetime, timezone
from fastapi import Depends, APIRouter
from starlette.responses import JSONResponse

from ...core.errors.auth_errors import TokenInvalidError
from ...database.session_manager import get_db
from ...core.services.auth.auth_service import AuthService
from ...core.services.auth.token_service import TokenService
from ...core.services.auth.dependencies import RefreshTokenBearer
from ...schemas.auth.log_in import(
    StaffLoginRequest, StudentLoginRequest, GuardianLoginRequest
)
from ...schemas.enums import UserType


token_service=TokenService()
refresh = RefreshTokenBearer()

router = APIRouter()

@router.post("/staff/login")
async def staff_login(login_data: StaffLoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.log_in(
        identifier=login_data.email,
        password=login_data.password,
        user_type=UserType.STAFF
    )

@router.post("/student/login")
async def student_login(login_data: StudentLoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.log_in(
        identifier=login_data.student_id,
        password=login_data.password,
        user_type=UserType.STUDENT
    )

@router.post("/guardian/login")
async def guardian_login(login_data: GuardianLoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.log_in(
        identifier=login_data.identifier,
        password=login_data.password,
        user_type=UserType.GUARDIAN
    )

@router.get('refresh_token')
def refresh_token(token_details: dict = Depends(refresh)):
    expiry = token_details['exp']

    if datetime.fromtimestamp(expiry, tz=timezone.utc) > datetime.now(tz=timezone.utc):
        new_access_token = token_service.create_access_token(
            user_data = token_details['user']
        )
        return JSONResponse(content ={
            "access_token": new_access_token
        })

    raise TokenInvalidError
