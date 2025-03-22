from ..common_imports import *
from ..enums import DocumentType, ArchiveReason


class StudentDocumentBase(BaseModel):
    """Base model for student documents"""
    owner_id: UUID
    title: str
    academic_year: int
    document_type: DocumentType
    file_url: str

    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
            "owner_id": "00000000-0000-0000-0000-000000000001",
            "title": "First Term Report Card",
            "academic_year": 2024,
            "document_type": "RESULT",
            "file_url": "https://example.com/documents/report-card.pdf"
        }
    }


class StudentDocumentCreate(StudentDocumentBase):
    """Used for creating new student documents"""
    pass


class StudentDocumentUpdate(BaseModel):
    """Used for updating student documents"""
    title: str
    file_url: str


class StudentDocumentResponse(StudentDocumentBase):
    """Response model for student documents"""
    pass


class StudentDocumentInDB(StudentDocumentBase):
    """Represents stored student documents"""
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
            "title": "First Term Report Card",
            "academic_year": 2024,
            "document_type": "RESULT",
            "file_url": "https://example.com/documents/report-card.pdf",
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