from ..common_imports import *
from ..enums import ArchiveReason, ClassCode


class ClassBase(BaseModel):
    """Base model for class levels"""
    level_id: UUID
    code: ClassCode
    mentor_id: UUID
    student_rep_id: UUID
    assistant_rep_id: UUID
    order: int | None = None

    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
            "level_id": "00000000-0000-0000-0000-000000000000",
            "code": "A",
            "mentor_id": "00000000-0000-0000-0000-000000000000",
            "student_rep_id": "00000000-0000-0000-0000-000000000000",
            "assistant_rep_id": "00000000-0000-0000-0000-000000000000",
        }}

class ClassUpdate(ClassBase):
    """Used for updating class levels"""
    pass


class ClassCreate(ClassBase):
    """Used for creating new class levels"""
    pass


class ClassResponse(ClassBase):
    """Response model for class levels"""
    pass


class ClassInDB(ClassBase):
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

    json_schema_extra = {
        "example": {
            "id": "00000000-0000-0000-0000-000000000000",
            "level_id": "00000000-0000-0000-0000-000000000000",
            "code": "A",
            "mentor_id": "00000000-0000-0000-0000-000000000000",
            "student_rep_id": "00000000-0000-0000-0000-000000000000",
            "assistant_rep_id": "00000000-0000-0000-0000-000000000000",
            "order": "1",
            "created_at": "2024-02-17T12:00:00Z",
            "created_by": "00000000-0000-0000-0000-000000000000",
            "last_modified_at": "2024-02-17T12:00:00Z",
            "last_modified_by": "00000000-0000-0000-0000-000000000000",
            "is_archived": False,
            "archived_at": None,
            "archived_by": None,
            "archive_reason": None
        }}

