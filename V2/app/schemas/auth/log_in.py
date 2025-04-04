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

