
from V2.app.core.shared.schemas.enums import Term
from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *


class TotalGradeFilterParams(BaseFilterParams):
    name: Optional[str] = None
    order_by: Literal["order", "created_at"] = "order"



class TotalGradeBase(BaseModel):
    """Base model for total grades"""
    student_id: UUID
    academic_level_subject_id: UUID
    academic_session: str
    term: Term
    total_score: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "student_id": "00000000-0000-0000-0000-000000000001",
                "academic_level_subject_id": "00000000-0000-0000-0000-000000000002",
                "academic_session": "2025/2026",
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
