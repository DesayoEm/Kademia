from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ...database.session import get_db
from ...database.redis.tokens import token_blocklist
from ...core.services.auth.auth_service import AuthService
from ...core.services.auth.token_service import TokenService
from ...core.services.auth.password_service import PasswordService
from ...core.services.auth.dependencies import (
    RefreshTokenBearer, AccessTokenBearer, get_current_user
)
from ...schemas.auth.log_in import(
    StaffLoginRequest, StudentLoginRequest, GuardianLoginRequest
)
from ...schemas.auth.password_change import PasswordChange
from ...schemas.enums import UserType



token_service=TokenService()
refresh = RefreshTokenBearer()
access = AccessTokenBearer()

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
    return token_service.refresh_token(token_details)

@router.post("/change-password")
def change_password(
        password_data: PasswordChange,user = Depends(get_current_user()),
        token_data: dict = Depends(access),db: Session = Depends(get_db)):

    password_service = PasswordService(db)
    token_jti = token_data.get('jti')

    password_service.change_password(
        user,
        password_data.current_password,
        password_data.new_password,
        token_jti
    )
    return {"message": "Password changed successfully"}


@router.post("/logout")
async def logout(token_data: dict = Depends(access)):
    token_blocklist.revoke_token(token_data)
    return {"message": "Successfully logged out"}

