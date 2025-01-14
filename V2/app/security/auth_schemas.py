from ..schemas.common_imports import *
from ..schemas.enums import AccessLevel


class AccessLevelChangeRequest(BaseModel):
    user_id: UUID
    new_level: AccessLevel
    reason: str

class AccessLevelResponse(BaseModel):
    user_id: UUID
    previous_level: AccessLevel
    new_level: AccessLevel
    changed_at: datetime
    changed_by: UUID
    reason: str

    class Config:
        from_attributes = True