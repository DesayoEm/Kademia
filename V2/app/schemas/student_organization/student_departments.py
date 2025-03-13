from ..common_imports import *
from ..shared_models import *


class DepartmentFilterParams(BaseFilterParams):
    name: Optional[str] = None
    description: Optional[str] = None
    order_by: Literal["name", "created_at"] = "name"

class DepartmentBase(BaseModel):
    """Base model for class levels"""
    name: str
    description: str
    mentor_id: UUID | None = None
    student_rep_id: UUID | None = None
    assistant_rep_id: UUID | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
        "example": {
            "name": "Science",
            "description": "Science Classes"
        }}
        )

class DepartmentUpdate(DepartmentBase):
    """Used for updating class levels"""
    pass


class DepartmentCreate(DepartmentBase):
    """Used for creating new class levels"""
    pass


class DepartmentResponse(DepartmentBase):
    """Response model for class levels"""
    pass


class DepartmentInDB(DepartmentBase):
    """Represents stored class levels"""
    id: UUID
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
        "example": {
            "id": "00000000-0000-0000-0000-000000000000",
            "name": "Science",
            "description": "Science Classes",
            "mentor_id": "00000000-0000-0000-0000-000000000000",
            "student_rep_id": "00000000-0000-0000-0000-000000000000",
            "assistant_rep_id": "00000000-0000-0000-0000-000000000000",
            "order": "1",
            "created_by": "00000000-0000-0000-0000-000000000000",
            "last_modified_by": "00000000-0000-0000-0000-000000000000",
            "is_archived": False,
            "archived_at": None,
            "archived_by": None,
            "archive_reason": None
        }}
        )

