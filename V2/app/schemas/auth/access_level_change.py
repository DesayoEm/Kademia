from ..common_imports import *
from ..enums import AccessLevel


class AccessLevelChangeBase(BaseModel):
    """Base model for access level changes"""
    staff_id: UUID
    previous_level: AccessLevel
    new_level: AccessLevel
    reason: str
    changed_by: UUID
    changed_at: datetime

    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
            "staff_id": "00000000-0000-0000-0000-000000000001",
            "previous_level": "USER",
            "new_level": "ADMIN",
            "reason": "Promotion to department head",
            "changed_by": "00000000-0000-0000-0000-000000000002",
            "changed_at": "2024-02-17T12:00:00Z"
        }
    }


class AccessLevelChangeCreate(AccessLevelChangeBase):
    """Used for creating new access level changes"""
    pass


class AccessLevelChangeUpdate(BaseModel):
    """Used for updating access level changes"""
    reason: str


class AccessLevelChangeResponse(AccessLevelChangeBase):
    """Response model for access level changes"""
    pass


class AccessLevelChangeInDB(AccessLevelChangeBase):
    """Represents stored access level changes"""
    id: UUID

    json_schema_extra = {
        "example": {
            "id": "00000000-0000-0000-0000-000000000000",
            "staff_id": "00000000-0000-0000-0000-000000000001",
            "previous_level": "USER",
            "new_level": "ADMIN",
            "reason": "Promotion to department head",
            "changed_by": "00000000-0000-0000-0000-000000000002",
            "changed_at": "2024-02-17T12:00:00Z"
        }
    }