from ..common_imports import *
from ..shared_models import *


class StaffLogin(BaseModel):
    """Base model for staff login"""
    email_address: str
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "email_address": "aina.folu@example.com",
                "password": "pIEG0%FvRa",
            }
        })

