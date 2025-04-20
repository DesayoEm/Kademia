from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.enums import Term, ArchiveReason


class TotalGradeBase(BaseModel):
    """Base model for total grades"""
    student_id: UUID
    subject_id: UUID
    academic_year: str
    term: Term
    total_score: int
    rank: int | None = None

    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
            "student_id": "00000000-0000-0000-0000-000000000001",
            "subject_id": "00000000-0000-0000-0000-000000000002",
            "academic_year": "2023-2024",
            "term": "FIRST",
            "total_score": 85,
            "rank": 3
        }
    }


class TotalGradeCreate(TotalGradeBase):
    """Used for creating new total grades"""
    pass


class TotalGradeUpdate(BaseModel):
    """Used for updating total grades"""
    total_score: int
    rank: int | None


class TotalGradeResponse(TotalGradeBase):
    """Response model for total grades"""
    pass


class TotalGradeInDB(TotalGradeBase):
    """Represents stored total grades"""
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
            "student_id": "00000000-0000-0000-0000-000000000001",
            "subject_id": "00000000-0000-0000-0000-000000000002",
            "academic_year": "2023-2024",
            "term": "FIRST",
            "total_score": 85,
            "rank": 3,
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