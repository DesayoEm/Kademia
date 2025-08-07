from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.enums import ApprovalStatus
from app.core.shared.schemas.shared_models import *

class PromotionFilterParams(BaseFilterParams):
    student_id: UUID | None = None
    status_completed_by: UUID | None = None
    academic_session: str | None = None
    status: ApprovalStatus | None = None
    order_by: Literal["academic_session", "created_at"] = "academic_session"


class GraduationCreate(BaseModel):
    """Base model for student promotions"""
    academic_session: str


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "academic_session": "2025/2026"
            }
        }
    )

class PromotionBase(BaseModel):
    """Base model for student promotions"""
    academic_session: str
    notes: str


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "academic_session": "2025/2026",
                "notes": "Met promotion criteria"

            }
        }
    )


class PromotionCreate(PromotionBase):
    """For creating a new student promotion"""
    pass


class PromotionReview(BaseModel):
    """For updating a  promotion record"""
    academic_session: str
    notes: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "academic_session": "2025/2026",
                "notes": "Under review"

            }
        }
    )


class PromotionDecision(BaseModel):
    status: ApprovalStatus
    decision_reason: str | None = None
    

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "decision_reason": "agree",
                "status": "APPROVED",
                

            }
        }
    )
    
    
    
class PromotionResponse(PromotionBase):
    """Response model for student promotions"""
    student_id: UUID
    previous_level_id: UUID
    status: ApprovalStatus
    status_completed_by: UUID | None = None
    status_completed_at: datetime | None = None
    decision_reason: str | None = None
    notes: str | None = None

    
    
    
class PromotionAudit(BaseModel):
    """Response model for student promotions"""
    created_at: datetime | None = None
    created_by: UUID
    last_modified_at: datetime | None = None
    last_modified_by: UUID
    last_login: datetime | None = None
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None