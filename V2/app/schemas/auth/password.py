from ..common_imports import *
from ..enums import UserType
from ..shared_models import *

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
            "example": {
                "current_password": "xxxxxxxxxx",
                "new_password": "Kincaid@22"
            }
        }
    )

class ForgotPassword(BaseModel):
    identifier: str
    user_type: UserType

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "identifier": "xxxxxxxxxx",
                "user_type": "STUDENT"
            }
        }
    )

class PasswordResetRequest(BaseModel):
    token: str
    identifier: str
    new_password: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "token": "xxxxxxxxxx",
                "identifier": "xxxxxxxxxx",
                "new_password": "xxxxxxxxxx"
            }
        }
    )