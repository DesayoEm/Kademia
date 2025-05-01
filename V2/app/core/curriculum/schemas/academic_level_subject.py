from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *


class AcademicLevelSubjectFilterParams(BaseFilterParams):
    level_id: str|None = None
    subject_id: str | None = None
    educator_id: str | None = None
    is_elective: str | None = None
    session_year: str | None = None


class AcademicLevelSubjectBase(BaseModel):
    """Base model for academic level subject assignments"""
    level_id: UUID
    subject_id: UUID
    is_elective: bool = True
    educator_id: UUID | None = None
    session_year: str | None = None
    curriculum_url: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "level_id": "00000000-0000-0000-0000-000000000001",
                "subject_id": "00000000-0000-0000-0000-000000000002",
                "is_elective": True,
                "session_year": "2023-2024",
            }
        }
    )

class AcademicLevelSubjectResponse(AcademicLevelSubjectBase):
    """Response model for academic level subject assignments"""
    pass


class AcademicLevelSubjectCreate(AcademicLevelSubjectBase):
     """For creating new academic level subject assignments"""


class AcademicLevelSubjectUpdate(AcademicLevelSubjectBase):
    """For updating academic level subject assignments"""
    is_elective: bool = True
    session_year: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "is_elective": True,
                "session_year": "2023-2024",
            }
        }
    )


class AcademicLevelSubjectInDB(AcademicLevelSubjectBase):
    """Represents stored academic level subject assignments"""
    id: UUID
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None

