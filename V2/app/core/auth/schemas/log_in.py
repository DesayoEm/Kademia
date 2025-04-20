from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *

class StaffLoginRequest(BaseModel):
    email: EmailStr
    password: str

class StudentLoginRequest(BaseModel):
    student_id: str
    password: str

class GuardianLoginRequest(BaseModel):
    identifier: str
    password: str

