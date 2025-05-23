from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.enums import ApprovalStatus
from V2.app.core.shared.schemas.shared_models import *


class GraduationFilterParams(BaseFilterParams):
    academic_session: str | None = None
    status: ApprovalStatus | None = None
    order_by: Literal["academic_session", "created_at"] = "academic_session"


class GraduationBase(BaseModel):
    """Base model for student graduations"""
    academic_session: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    status_updated_by: UUID | None = None
    status_updated_at: datetime | None = None
    rejection_reason: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "academic_session": "2025/2026",
                "status": "PENDING"
            }
        }
    )


class GraduationCreate(GraduationBase):
    """For creating a new graduation record"""
    pass


class GraduationResponse(GraduationBase):
    """Response model for student graduations"""
    student_id: UUID
