from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from ...database.script import session
from fastapi import Depends, APIRouter
from ...database.session_manager import get_db
from ...crud.student_organization.academic_levels import AcademicLevelCrud
from ...core.services.auth.auth_service import AuthService
from ...core.services.auth.token_service import TokenService
from ...schemas.auth.staff_auth import StaffLogin
from fastapi.responses import JSONResponse


token_service=TokenService()

router = APIRouter()


@router.post("/login")
def login(
        login_data: StaffLogin,
        db: Session = Depends(get_db)
):
    auth = AuthService(db)
    staff = auth.authenticate_staff(login_data.email_address, login_data.password)

    if not staff:
        return JSONResponse(content={"message": "Failed authentication"}, status_code=401)

    access_token = token_service.create_access_token(
        user_data={
            'email': login_data.email_address,
            'user_uid': "tr(login_data.uid)"
            # 'user_uid': str(login_data.uid)
        }
    )
    refresh_token = token_service.create_access_token(
        user_data={
            'email': login_data.email_address,
            'user_uid': "tr(login_data.uid)"
            # 'user_uid': str(login_data.uid)
        },
        refresh=True,
        expiry=timedelta(days=2)
    )

    return JSONResponse(
        content={
            "message": "Successful",
            "access_token": access_token,
            "refresh_token": refresh_token
        },
        status_code=200
    )
