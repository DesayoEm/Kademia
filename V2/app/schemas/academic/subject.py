from ..common_imports import *
from ..enums import ArchiveReason


class SubjectBase(BaseModel):
    """Base model for subjects"""
    name: str
    department_id: UUID
    is_elective: bool = False
    syllabus_url: str | None = None

    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
            "name": "Mathematics",
            "department_id": "00000000-0000-0000-0000-000000000001",
            "is_elective": False,
            "syllabus_url": "https://example.com/syllabus/math"
        }
    }


class SubjectCreate(SubjectBase):
    """Used for creating new subjects"""
    pass


class SubjectUpdate(BaseModel):
    """Used for updating subjects"""
    name: str
    is_elective: bool
    syllabus_url: str | None


class SubjectResponse(SubjectBase):
    """Response model for subjects"""
    pass


class SubjectInDB(SubjectBase):
    """Represents stored subjects"""
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
            "name": "Mathematics",
            "department_id": "00000000-0000-0000-0000-000000000001",
            "is_elective": False,
            "syllabus_url": "https://example.com/syllabus/math",
            "created_at": "2024-02-17T12:00:00Z",
            "created_by": "00000000-0000-0000-0000-000000000000",
            "last_modified_at": "2024-02-17T12:00:00Z",
            "last_modified_by": "00000000-0000-0000-0000-000000000000",
            "is_archived": False,
            "archived_at": None,
            "archived_by": None,
            "archive_reason": None
        }
    }