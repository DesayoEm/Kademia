from ..common_imports import *
from ..enums import Term, ArchiveReason


class StudentSubjectBase(BaseModel):
    """Base model for student subject enrollments"""
    student_id: UUID
    subject_id: UUID
    academic_year: str
    term: Term
    is_active: bool = True

    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
            "student_id": "00000000-0000-0000-0000-000000000001",
            "subject_id": "00000000-0000-0000-0000-000000000002",
            "academic_year": "2023-2024",
            "term": "FIRST",
            "is_active": True
        }
    }


class StudentSubjectUpdate(StudentSubjectBase):
    """Used for updating student subject enrollments"""
    pass


class StudentSubjectCreate(StudentSubjectBase):
    """Used for creating new student subject enrollments"""
    pass


class StudentSubjectResponse(StudentSubjectBase):
    """Response model for student subject enrollments"""
    pass


class StudentSubjectInDB(StudentSubjectBase):
    """Represents stored student subject enrollments"""
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
            "is_active": True,
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