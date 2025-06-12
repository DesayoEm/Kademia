from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter

from V2.app.infra.db.session_manager import get_db
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.password_service import PasswordService
from V2.app.core.auth.services.dependencies.token_deps import RefreshTokenBearer, AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_current_user

from V2.app.core.auth.schemas.password import (
    PasswordChange, PasswordResetRequest, ForgotPassword, PasswordResetData
)


token_service=TokenService()
refresh = RefreshTokenBearer()
access = AccessTokenBearer()
router = APIRouter()


@router.put("/change-password")
def change_password(
        password_data: PasswordChange,token_data: dict = Depends(access),
        db: Session = Depends(get_db)):

    user = get_current_user(token_data, db)
    password_service = PasswordService(db)

    password_service.change_password(
        user,
        password_data.current_password,
        password_data.new_password,
        token_data
    )
    return {"message": "Password changed successfully"}



@router.put("/forgot-password")
def forgot_password(data: ForgotPassword, db: Session = Depends(get_db)):
    password_service = PasswordService(db)

    return password_service.forgot_password(data.identifier, data.user_type)


@router.put("/request-password-reset")
def request_password_reset(data: PasswordResetRequest, db: Session = Depends(get_db)):
    password_service = PasswordService(db)

    password_service.request_password_reset(data.email_address)
    return {"message": "Please check your email for a reset link."}


@router.put("/reset-password")
def reset_password(data: PasswordResetData, db: Session = Depends(get_db)):

    password_service = PasswordService(db)
    password_service.reset_password(
            password_token=data.token,
            new_password=data.new_password
        )
    return {"message": "Password has been successfully reset."}
