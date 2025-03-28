from ..common_imports import *
from ..shared_models import *

class PasswordChange(BaseModel):
    current_password: str
    new_password: str