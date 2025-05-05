
from V2.app.core.shared.schemas.enums import Term, GradeType
from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *

class GradeFilterParams(BaseFilterParams):
    type: GradeType | None = None
    term: Term | None = None
    order_by: Literal["order", "created_at"] = "order"
    academic_session: str | None = None
    graded_on: date


class GradeBase(BaseModel):
    """Base model for student grades"""
    academic_session: str
    term: Term
    weight: float
    type: GradeType
    score: int
    graded_by: UUID
    graded_on:date


class GradeCreate(GradeBase):
    """Used for creating new student grades"""


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "academic_session": "2025/2026",
                "weight": 5.0,
                "term": "FIRST",
                "type": "EXAM",
                "score": 85,
                "feedback": "Excellent work on calculus section",
                "graded_by": "00000000-0000-0000-0000-000000000003",
                "graded_on": "2025-12-06"
            }
        }

    )

class GradeUpdate(GradeBase):
    """For updating student grades"""

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "academic_session": "2025/2026",
                "term": "FIRST",
                "type": "EXAM",
                "score": 25,
                "feedback": "Algebra knowledge needs to be worked on",
                "graded_by": "00000000-0000-0000-0000-000000000003"
            }
        }

    )

class GradeResponse(GradeCreate):
    """Response model for student grades"""
    file_url: str | None = None
    feedback: str | None = None
    student_id: UUID

