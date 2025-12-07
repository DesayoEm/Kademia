from app.core.shared.schemas.enums import Semester
from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.shared_models import *


class TotalGradeFilterParams(BaseFilterParams):
    student_id: UUID | None = None
    student_subject_id: UUID | None = None

    order_by: Literal["order", "created_at"] = "order"


class TotalGradeBase(BaseModel):
    """Base model for total grades"""

    total_score: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class TotalGradeCreate(TotalGradeBase):
    """For creating new total grades"""

    pass


class TotalGradeResponse(TotalGradeBase):
    """Response model for total grades"""

    rank: int | None = None


class TotalGradeAudit(BaseModel):
    """Response model for total grade object audit"""

    id: UUID
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason
