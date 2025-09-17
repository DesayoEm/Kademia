from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.shared_models import *
from app.core.shared.schemas.enums import UserRole

class RoleHistoryFilterParams(BaseFilterParams):
    changed_by_id: UUID | None = None
    staff_id: UUID | None = None


class RoleHistoryBase(BaseModel):
    """Base model for access role changes"""
    new_role: UserRole
    reason: str


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "new_role": "SUPERUSER",
                "reason": "Promotion"
            }
        }
    )


class RoleHistoryCreate(RoleHistoryBase):
    """For creating new access role changes"""
    pass


class RoleHistoryResponse(RoleHistoryBase):
    """Response model for access role changes"""
    previous_role: UserRole



class RoleHistoryAudit(RoleHistoryBase):
    """Response model for access role changes"""
    staff_id: UUID
    changed_at: datetime
    changed_by_id: UUID


