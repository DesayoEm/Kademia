from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *
from V2.app.core.shared.schemas.enums import Term


class StudentSubjectFilterParams(BaseFilterParams):
    academic_session: str | None = None
    term: str | None = None
    is_active: bool | None = None

    order_by: Literal["created_at"] = "created_at"

class StudentSubjectBase(BaseModel):
    """Base model for student subject enrollments"""
    academic_level_subject_id: UUID
    academic_session: str
    term: Term
    is_active: bool = True

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "academic_level_subject_id": "00000000-0000-0000-0000-000000000002",
                "academic_session": "2023-2024",
                "term": "FIRST",
                "is_active": True
            }
        }
    )

class StudentSubjectCreate(StudentSubjectBase):
    """Used for creating new student subject enrollments"""
    pass


class StudentSubjectResponse(StudentSubjectBase):
    """Response model for student subject enrollments"""
    pass

