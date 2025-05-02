from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.enums import Term, GradeType, ArchiveReason


class GradeBase(BaseModel):
    """Base model for student grades"""
    session_year: str
    term: Term
    weight: float
    type: GradeType
    score: int
    graded_by: UUID
    graded_on:date


class GradeCreate(GradeBase):
    """Used for creating new student grades"""
    student_id: UUID
    subject_id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "student_id": "00000000-0000-0000-0000-000000000001",
                "subject_id": "00000000-0000-0000-0000-000000000002",
                "academic_year": "2025/2026",
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
                "academic_year": "2025/2026",
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

