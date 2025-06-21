from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.enums import ApprovalStatus
from V2.app.core.shared.schemas.shared_models import *


class RepetitionFilterParams(BaseFilterParams):
    academic_session: str | None = None
    status: ApprovalStatus | None = None
    order_by: Literal["academic_session", "created_at"] = "academic_session"


class StudentRepetitionBase(BaseModel):
    """Base model for student repetitions"""
    academic_session: str
    repeat_level_id: UUID
    repetition_reason: str
    status: ApprovalStatus = ApprovalStatus.PENDING


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
                "example": {
                    "academic_session": "2025/2026",
                    "repeat_level_id": "00000000-0000-0000-0000-000000000002",
                    "repetition_reason": "Academic performance below promotion criteria"
                }
            }

   )


class StudentRepetitionReview(BaseModel):
    """Model for reviewing student repetitions"""
    repeat_level_id: UUID
    repetition_reason: str


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
                "example": {
                    "repeat_level_id": "00000000-0000-0000-0000-000000000002",
                    "repetition_reason": "Academic performance below promotion criteria"
                }
            }

   )


class StudentRepetitionDecision(BaseModel):
    """Model for reviewing student repetitions"""
    status: ApprovalStatus = ApprovalStatus.PENDING
    decision_reason: str


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
                "example": {
                    "decision_reason": "Academic performance below promotion criteria",
                    "status": "APPROVED"
                }
            }

   )


class StudentRepetitionCreate(StudentRepetitionBase):
    """For creating a new student repetition"""
    pass


class StudentRepetitionResponse(StudentRepetitionBase):
    """Response model for student repetitions"""
    student_id: UUID
    failed_level_id: UUID
    status_completed_by: UUID | None = None
    status_completed_at: datetime | None = None
    decision_reason: str | None = None


class StudentRepetitionAudit(StudentRepetitionBase):
    """Response model for student repetitions"""
    created_at: datetime | None = None
    created_by: UUID
    last_modified_at: datetime | None = None
    last_modified_by: UUID
    last_login: datetime | None = None
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None
