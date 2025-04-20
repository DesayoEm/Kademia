from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *
from V2.app.core.shared.schemas.enums import ArchiveReason, ClassCode

class ClassCodeRequest(BaseModel):
    reason: ClassCode

class ClassFilterParams(BaseFilterParams):
    level_id: UUID | None = None
    code: str |None = None
    order_by: Literal["order", "created_at"] = "order"


class ClassBase(BaseModel):
    """Base model for class levels"""
    level_id: UUID
    code: ClassCode



    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
        "example": {
            "level_id": "00000000-0000-0000-0000-000000000000",
            "code": "A"

        }}
    )

class ClassUpdate(BaseModel):
    """Used for updating class levels"""

    order: int |None = None
    code: ClassCode | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "order": "0",
                "code": "B"
            }}
    )

class ClassCreate(ClassBase):
    """Used for creating new class levels"""
    pass


class ClassResponse(ClassBase):
    """Response model for class levels"""
    order: int


class ClassInDB:
    """Represents stored class levels"""
    id: UUID
    level_id: UUID
    code: ClassCode
    order: int
    supervisor_id: UUID | None = None
    student_rep_id: UUID | None = None
    assistant_rep_id: UUID | None = None
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None


