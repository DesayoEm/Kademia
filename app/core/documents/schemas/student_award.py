
from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.enums import DocumentType
from app.core.shared.schemas.shared_models import *


class AwardFilterParams(BaseFilterParams):
    student_id: UUID|None = None
    title: str|None = None
    document_type: DocumentType | None = None
    academic_session: str|None = None
    order_by: Literal["title", "created_at"] = "title"


class AwardBase(BaseModel):
    """Base model for student awards"""
    title: str
    description: str|None = None
    academic_session: str


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "title": "Outstanding Academic Achievement",
                "description": "Awarded for maintaining highest Math Score in the class",
                "academic_session": "2025/2026",

            }
        }
    )


class AwardUpdate(BaseModel):
    """Used for updating student awards"""
    title: str | None = None
    description: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "title": "Outstanding Academic Achievement",
                "description": "Awarded for maintaining highest Math Score in the class"

            }
        }
    )


class AwardCreate(AwardBase):
    """Used for creating new student awards"""
    pass


class AwardResponse(AwardBase):
    """Response model for student awards"""
    award_s3_key: str|None = None


class AwardAudit(BaseModel):
    """Response model for student awards audit"""
    id: UUID
    student_id: UUID
    award_s3_key: str | None = None
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None