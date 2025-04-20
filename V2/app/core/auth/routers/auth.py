from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from V2.app.core.shared.database import get_db
from V2.app.core.shared.database import token_blocklist
from ...core.services.auth.auth_service import AuthService
from ...core.services.auth.token_service import TokenService
from ...core.services.auth.dependencies import (
    RefreshTokenBearer, AccessTokenBearer
)
from V2.app.core.auth.schemas.log_in import(
    StaffLoginRequest, StudentLoginRequest, GuardianLoginRequest
)
from V2.app.core.shared.schemas.enums import UserType



token_service=TokenService()
refresh = RefreshTokenBearer()
access = AccessTokenBearer()

router = APIRouter()

@router.post("/staff/login")
async def staff_login(login_data: StaffLoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.log_in(
        identifier=login_data.email,password=login_data.password,user_type=UserType.STAFF
    )

@router.post("/student/login")
async def student_login(login_data: StudentLoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.log_in(
        identifier=login_data.student_id, password=login_data.password, user_type=UserType.STUDENT
    )

@router.post("/guardian/login")
async def guardian_login(login_data: GuardianLoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.log_in(
        identifier=login_data.identifier, password=login_data.password, user_type=UserType.GUARDIAN
    )


@router.get('/refresh_token')
def refresh_token(token_details: dict = Depends(refresh)):
    return token_service.refresh_token(token_details)


@router.post("/logout")
async def logout(token_data: dict = Depends(access)):
    token_blocklist.revoke_token(token_data)
    return {"message": "Successfully logged out"}

