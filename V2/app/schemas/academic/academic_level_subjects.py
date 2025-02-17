from ..common_imports import *
from ..enums import ArchiveReason


class AcademicLevelSubjectBase(BaseModel):
    """Base model for academic level subject assignments"""
    level_id: UUID
    subject_id: UUID
    educator_id: UUID
    is_elective: bool = False
    academic_year: str
    curriculum_url: str

    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
            "level_id": "00000000-0000-0000-0000-000000000001",
            "subject_id": "00000000-0000-0000-0000-000000000002",
            "educator_id": "00000000-0000-0000-0000-000000000003",
            "is_elective": False,
            "academic_year": "2023-2024",
            "curriculum_url": "https://example.com/curriculum/math-jss1"
        }
    }


class AcademicLevelSubjectUpdate(AcademicLevelSubjectBase):
    """Used for updating academic level subject assignments"""
    pass


class AcademicLevelSubjectCreate(AcademicLevelSubjectBase):
    """Used for creating new academic level subject assignments"""
    pass


class AcademicLevelSubjectResponse(AcademicLevelSubjectBase):
    """Response model for academic level subject assignments"""
    pass


class AcademicLevelSubjectInDB(AcademicLevelSubjectBase):
    """Represents stored academic level subject assignments"""
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
            "level_id": "00000000-0000-0000-0000-000000000001",
            "subject_id": "00000000-0000-0000-0000-000000000002",
            "educator_id": "00000000-0000-0000-0000-000000000002",
            "is_elective": False,
            "academic_year": "2023-2024",
            "curriculum_url": "https://example.com/curriculum/math-jss1",
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