from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *
from V2.app.core.shared.schemas.enums import Term

class SubjectEducatorFilterParams(BaseFilterParams):
    educator_id: UUID|None = None
    subject_id: UUID | None = None
    level_id: UUID | None = None
    session_year: str | None = None
    term: Term | None = None
    is_active: bool | None = None
    date_assigned: date| None = None

    order_by: Literal["created_at"] = "created_at"


class SubjectEducatorBase(BaseModel):
    """Base model for subject educator assignments"""
    subject_id: UUID
    educator_id: UUID
    level_id: UUID
    session_year: str
    term: Term
    is_active: bool = False
    date_assigned: date

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "subject_id": "00000000-0000-0000-0000-000000000001",
                "educator_id": "00000000-0000-0000-0000-000000000002",
                "level_id": "00000000-0000-0000-0000-000000000003",
                "session_year": "2023-2024",
                "term": "FIRST",
                "is_active": True,

            }
        }
    )


class SubjectEducatorCreate(SubjectEducatorBase):
    """Used for creating new subject educator assignments"""
    pass


class SubjectEducatorResponse(SubjectEducatorBase):
    """Response model for subject educator assignments"""
    pass


