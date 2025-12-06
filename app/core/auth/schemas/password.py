from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.enums import UserType
from app.core.shared.schemas.shared_models import *


class PasswordChange(BaseModel):
    current_password: str
    new_password: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {"current_password": "xxxxxxxxxx", "new_password": "Kincaid@22"}
        },
    )


class ForgotPassword(BaseModel):
    identifier: str
    user_type: UserType

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {"identifier": "xxxxxxxxxx", "user_type": "STUDENT"}
        },
    )


class PasswordResetRequest(BaseModel):
    email_address: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "email_address": "xxxxxxxxxx",
            }
        },
    )


class PasswordResetData(BaseModel):
    token: str
    new_password: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {"token": "xxxxxxxxxx", "new_password": "xxxxxxxxxx"}
        },
    )
