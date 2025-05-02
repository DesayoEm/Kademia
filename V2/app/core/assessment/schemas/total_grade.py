from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.enums import Term


class TotalGradeBase(BaseModel):
    """Base model for total grades"""
    student_id: UUID
    subject_id: UUID
    session_year: str
    term: Term
    total_score: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "student_id": "00000000-0000-0000-0000-000000000001",
                "subject_id": "00000000-0000-0000-0000-000000000002",
                "session_year": "2025/2026",
                "term": "FIRST",
                "total_score": 85,
            }
        }
    )

class TotalGradeCreate(TotalGradeBase):
    """For creating new total grades"""
    pass


class TotalGradeResponse(TotalGradeBase):
    """Response model for total grades"""
    rank: int | None = None
