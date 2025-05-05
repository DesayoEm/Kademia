from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *
from V2.app.core.shared.schemas.enums import AccessLevel

class AccessLevelFilterParams(BaseFilterParams):
    changed_by_id: UUID | None = None


class AccessLevelChangeBase(BaseModel):
    """Base model for access level changes"""
    new_level: AccessLevel
    reason: str


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "new_level": "SUPERUSER",
                "reason": "Promotion to department head"
            }
        }
    )


class AccessLevelChangeCreate(AccessLevelChangeBase):
    """For creating new access level changes"""
    pass


class AccessLevelChangeResponse(AccessLevelChangeBase):
    """Response model for access level changes"""
    previous_level: AccessLevel
    changed_by_id: UUID
    changed_at: datetime
    staff_id: UUID

