from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.shared_models import *
from app.core.shared.schemas.enums import Semester


class SubjectEducatorFilterParams(BaseFilterParams):
    academic_session: str | None = None
    academic_level_subject_id: UUID | None = None
    educator_id: UUID | None = None
    semester: Semester | None = None
    is_active: bool | None = None
    date_assigned: date | None = None

    order_by: Literal["created_at"] = "created_at"


class SubjectEducatorBase(BaseModel):
    """Base model for subject educator assignments"""

    academic_level_subject_id: UUID
    academic_session: str | None = None
    is_active: bool = True

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "academic_level_subject_id": "00000000-0000-0000-0000-000000000001",
                "academic_session": "2025/2026",
                "semester": "FIRST",
                "is_active": True,
            }
        },
    )


class SubjectEducatorCreate(SubjectEducatorBase):
    """Used for creating new subject educator assignments"""

    pass


class SubjectEducatorResponse(SubjectEducatorBase):
    """Response model for subject educator assignments"""

    date_assigned: date


class SubjectEducatorAudit(BaseModel):
    """Response model for subject audit"""

    id: UUID
    academic_level_subject_id: UUID
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None
