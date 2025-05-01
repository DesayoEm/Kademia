from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.enums import Term, ArchiveReason


class SubjectEducatorBase(BaseModel):
    """Base model for subject educator assignments"""
    subject_id: UUID
    educator_id: UUID
    level_id: UUID
    academic_year: str
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
                "academic_year": "2023-2024",
                "term": "FIRST",
                "is_active": True,
                "date_assigned": "2024-02-17"
            }
        }
    )



class SubjectEducatorCreate(SubjectEducatorBase):
    """Used for creating new subject educator assignments"""
    pass


class SubjectEducatorUpdate(BaseModel):
    """Used for updating subject educator assignments"""
    is_active: bool
    date_assigned: date


class SubjectEducatorResponse(SubjectEducatorBase):
    """Response model for subject educator assignments"""
    pass


class SubjectEducatorInDB(SubjectEducatorBase):
    """Represents stored subject educator assignments"""
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
            "subject_id": "00000000-0000-0000-0000-000000000001",
            "educator_id": "00000000-0000-0000-0000-000000000002",
            "level_id": "00000000-0000-0000-0000-000000000003",
            "academic_year": "2023-2024",
            "term": "FIRST",
            "is_active": True,
            "date_assigned": "2024-02-17",
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