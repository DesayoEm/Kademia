from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import Depends, APIRouter
from ...database.session_manager import get_db
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
    #authenticate
    staff = auth.authenticate_staff(login_data.email_address, login_data.password)

    #generate tokens
    access_token = token_service.create_access_token(
        user_data={
            'email': login_data.email_address,
            'user_id': str(staff.id),
            'user_type':staff.user_type,
            'staff_type':staff.staff_type,
            'access_level':staff.access_level,
        }
    )
    refresh_token = token_service.create_access_token(
        user_data={
            'email': login_data.email_address,
            'user_id': str(staff.id),
            'user_type': staff.user_type,
            'staff_type': staff.staff_type,
            'access_level': staff.access_level,
        },
        refresh=True,
        expiry=timedelta(days=1)
    )

    return JSONResponse(
        content={
            "message": "Successful",
            "access_token": access_token,
            "refresh_token": refresh_token
        },
        status_code=200
    )
