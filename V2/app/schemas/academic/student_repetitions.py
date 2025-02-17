from ..common_imports import *
from ..enums import ApprovalStatus, ArchiveReason


class StudentRepetitionBase(BaseModel):
    """Base model for student repetitions"""
    student_id: UUID
    academic_year: int
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
            "academic_year": 2024,
            "previous_level_id": "00000000-0000-0000-0000-000000000002",
            "new_level_id": "00000000-0000-0000-0000-000000000002",
            "previous_class_id": "00000000-0000-0000-0000-000000000003",
            "new_class_id": "00000000-0000-0000-0000-000000000004",
            "reason": "Academic performance below promotion criteria",
            "status": "PENDING",
            "status_updated_by": None,
            "status_updated_at": None,
            "rejection_reason": None
        }
    }


class StudentRepetitionCreate(StudentRepetitionBase):
    """Used for creating new student repetitions"""
    pass


class StudentRepetitionUpdate(BaseModel):
    """Used for updating student repetitions"""
    status: ApprovalStatus
    status_updated_by: UUID
    status_updated_at: datetime
    rejection_reason: str | None


class StudentRepetitionResponse(StudentRepetitionBase):
    """Response model for student repetitions"""
    pass


class StudentRepetitionInDB(StudentRepetitionBase):
    """Represents stored student repetitions"""
    id: UUID
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None

    json_schema_extra = {
        "example": {
            "id": "00000000-0000-0000-0000-000000000000",
            "student_id": "00000000-0000-0000-0000-000000000001",
            "academic_year": 2024,
            "previous_level_id": "00000000-0000-0000-0000-000000000002",
            "new_level_id": "00000000-0000-0000-0000-000000000002",
            "previous_class_id": "00000000-0000-0000-0000-000000000003",
            "new_class_id": "00000000-0000-0000-0000-000000000004",
            "reason": "Academic performance below promotion criteria",
            "status": "PENDING",
            "status_updated_by": None,
            "status_updated_at": None,
            "rejection_reason": None,
            "created_at": "2024-02-17T12:00:00Z",
            "created_by": "00000000-0000-0000-0000-000000000000",
            "last_modified_at": "2024-02-17T12:00:00Z",
            "last_modified_by": "00000000-0000-0000-0000-000000000000",
            "is_archived": False,
            "archived_at": None,
            "archived_by": None,
            "archive_reason": None
        }
    }