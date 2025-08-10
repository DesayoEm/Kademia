from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.shared_models import *


class AcademicLevelSubjectFilterParams(BaseFilterParams):
    is_elective: str | None = None
    academic_session: str | None = None
    subject_id: UUID | None = None
    level_id: UUID | None = None


class AcademicLevelSubjectBase(BaseModel):
    """Base model for academic level subject assignments"""
    subject_id: UUID
    code: str | None = None
    is_elective: bool = True



    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "subject_id": "00000000-0000-0000-0000-000000000002",
                "is_elective": True,
                "code": "BIO 222",
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

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "is_elective": True,
            }
        }
    )


class AcademicLevelSubjectAudit(BaseModel):
    """Response model for level subject audit"""
    id: UUID
    subject_id: UUID
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason
