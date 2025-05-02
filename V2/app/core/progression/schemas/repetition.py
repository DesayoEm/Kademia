from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.enums import ApprovalStatus, ArchiveReason


class StudentRepetitionBase(BaseModel):
    """Base model for student repetitions"""
    student_id: UUID
    session_year: str
    previous_level_id: UUID
    new_level_id: UUID
    previous_class_id: UUID
    new_class_id: UUID
    reason: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    status_updated_by: UUID | None = None
    status_updated_at: datetime | None = None
    rejection_reason: str | None = None

    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
            "student_id": "00000000-0000-0000-0000-000000000001",
            "session_year": "2025/2026",
            "previous_level_id": "00000000-0000-0000-0000-000000000002",
            "new_level_id": "00000000-0000-0000-0000-000000000002",
            "previous_class_id": "00000000-0000-0000-0000-000000000003",
            "new_class_id": "00000000-0000-0000-0000-000000000004",
            "reason": "Academic performance below promotion criteria",
            "status": "PENDING"

        }
    }


class StudentRepetitionCreate(StudentRepetitionBase):
    """For creating a new student repetition"""
    pass



class StudentRepetitionResponse(StudentRepetitionBase):
    """Response model for student repetitions"""
    pass

