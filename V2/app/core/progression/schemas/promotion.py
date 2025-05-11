from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.enums import ApprovalStatus
from V2.app.core.shared.schemas.shared_models import *

class PromotionFilterParams(BaseFilterParams):
    academic_session: str | None = None
    status: ApprovalStatus | None = None
    order_by: Literal["academic_session", "created_at"] = "academic_session"


class StudentPromotionBase(BaseModel):
    """Base model for student promotions"""
    academic_session: str
    new_level_id: UUID
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
                "new_level_id": "00000000-0000-0000-0000-000000000002",
                "status": "PENDING"
            }
        }
    )


class StudentPromotionCreate(StudentPromotionBase):
    """For creating a new student promotion"""
    pass


class StudentPromotionResponse(StudentPromotionBase):
    """Response model for student promotions"""
    student_id: UUID
    previous_level_id: UUID
    previous_class_id: UUID
