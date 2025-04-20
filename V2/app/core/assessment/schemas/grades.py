from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.enums import Term, GradeType, ArchiveReason


class GradeBase(BaseModel):
    """Base model for student grades"""
    student_id: UUID
    subject_id: UUID
    academic_year: str
    term: Term
    type: GradeType
    score: int
    file_url: str | None = None
    feedback: str | None = None
    graded_by: UUID


    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
            "student_id": "00000000-0000-0000-0000-000000000001",
            "subject_id": "00000000-0000-0000-0000-000000000002",
            "academic_year": "2023-2024",
            "term": "FIRST",
            "type": "EXAM",
            "score": 85,
            "file_url": "https://example.com/grades/math-exam.pdf",
            "feedback": "Excellent work on calculus section",
            "graded_by": "00000000-0000-0000-0000-000000000003"
        }
    }


class GradeUpdate(GradeBase):
    """Used for updating student grades"""
    pass


class GradeCreate(GradeBase):
    """Used for creating new student grades"""
    pass


class GradeResponse(GradeBase):
    """Response model for student grades"""
    pass


class GradeInDB(GradeBase):
    """Represents stored student grades"""
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
            "type": "EXAM",
            "score": 85,
            "file_url": "https://example.com/grades/math-exam.pdf",
            "feedback": "Excellent work on calculus section",
            "graded_by": "00000000-0000-0000-0000-000000000003",
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