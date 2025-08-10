from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.shared_models import *


class DepartmentFilterParams(BaseFilterParams):
    name: Optional[str] = None
    description: Optional[str] = None
    mentor_id: UUID|None = None
    order_by: Literal["name", "created_at"] = "name"


class DepartmentBase(BaseModel):
    """Base model for class levels"""
    name: str
    description: str
    code: str


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
        "example": {
            "name": "Science",
            "code": "SCI",
            "description": "Science Classes"
        }}
        )

class DepartmentUpdate(DepartmentBase):
    """Used for updating class levels"""
    name: str | None = None
    description: str | None = None
    code: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "name": "Science",
                "code": "SCC",
                "description": "Sciences"
            }}
    )

class DepartmentCreate(DepartmentBase):
    """Used for creating new class levels"""
    pass


class DepartmentResponse(DepartmentBase):
    """Response model for class levels"""
    mentor_id: UUID | None = None
    student_rep_id: UUID | None = None
    assistant_rep_id: UUID | None = None


class DepartmentAudit(BaseModel):
    """Department audit information"""
    id: UUID
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None




