from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ...database.session_manager import get_db
from ...core.services.auth.auth_service import AuthService
from ...core.services.auth.token_service import TokenService
from ...schemas.auth.log_in import(
    StaffLoginRequest, StudentLoginRequest, GuardianLoginRequest
)
from ...schemas.enums import UserType


token_service=TokenService()

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