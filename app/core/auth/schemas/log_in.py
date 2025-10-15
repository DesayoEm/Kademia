from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.shared_models import *

class StaffLoginRequest(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "email": "admin@kademia.com",
                "password": "kademia"
        }
    }
    )


class StudentLoginRequest(BaseModel):
    student_id: str
    password: str

class GuardianLoginRequest(BaseModel):
    identifier: str
    password: str

