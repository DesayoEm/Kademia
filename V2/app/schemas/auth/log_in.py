from ..common_imports import *
from ..shared_models import *

class StaffLoginRequest(BaseModel):
    email: EmailStr
    password: str

class StudentLoginRequest(BaseModel):
    student_id: str
    password: str

class GuardianLoginRequest(BaseModel):
    identifier: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user_info: dict