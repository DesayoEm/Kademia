from app.core.shared.schemas.enums import Semester, GradeType
from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.shared_models import *


class GradeFilterParams(BaseFilterParams):
    student_id: UUID | None = None
    student_subject_id: UUID | None = None
    graded_by: UUID | None = None
    type: GradeType | None = None
    graded_on: date | None = None
    order_by: Literal["order", "created_at"] = "order"


class GradeBase(BaseModel):
    """Base model for student grades"""

    weight: float
    type: GradeType
    score: int
    max_score: int
    graded_by: UUID
    graded_on: date
    feedback: str | None = None


class GradeCreate(GradeBase):
    """Used for creating new student grades"""

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "weight": 5.0,
                "type": "EXAM",
                "score": 85,
                "max_score": 100,
                "feedback": "Excellent work on calculus section",
                "graded_by": "00000000-0000-0000-0000-000000000003",
                "graded_on": "2025-07-06",
            }
        },
    )


class GradeUpdate(BaseModel):
    """For updating student grades"""

    weight: float | None = None
    type: GradeType | None = None
    score: int | None = None
    max_score: int | None = None
    graded_by: UUID | None = None
    graded_on: date | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "type": "EXAM",
                "score": 25,
                "max_score": 100,
                "feedback": "Algebra knowledge needs to be worked on",
                "graded_by": "00000000-0000-0000-0000-000000000003",
            }
        },
    )


class GradeResponse(GradeCreate):
    """Response model for student grades"""

    file_url: str | None = None
    feedback: str | None = None
    student_id: UUID


class GradeAudit(BaseModel):
    """Response model for grade object audit"""

    id: UUID
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None
