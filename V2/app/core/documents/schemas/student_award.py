from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.enums import ArchiveReason


class StudentAwardBase(BaseModel):
    """Base model for student awards"""
    owner_id: UUID
    title: str
    description: str
    academic_year: int
    file_url: str

    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
            "owner_id": "00000000-0000-0000-0000-000000000001",
            "title": "Outstanding Academic Achievement",
            "description": "Awarded for maintaining highest Math Score in the class",
            "academic_year": 2024,
            "file_url": "https://example.com/awards/certificate.pdf"
        }
    }


class StudentAwardUpdate(StudentAwardBase):
    """Used for updating student awards"""
    pass


class StudentAwardCreate(StudentAwardBase):
    """Used for creating new student awards"""
    pass


class StudentAwardResponse(StudentAwardBase):
    """Response model for student awards"""
    pass


class StudentAwardInDB(StudentAwardBase):
    """Represents stored student awards"""
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
            "owner_id": "00000000-0000-0000-0000-000000000001",
            "title": "Outstanding Academic Achievement",
            "description": "Awarded for maintaining the highest Math Score in the class",
            "academic_year": 2024,
            "file_url": "https://example.com/awards/certificate.pdf",
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