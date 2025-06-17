from V2.app.core.shared.schemas.enums import DocumentType
from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *


class DocumentFilterParams(BaseFilterParams):
    title: str|None = None
    owner_id: UUID|None = None
    academic_session: str|None = None
    document_type: DocumentType|None = None

    order_by: Literal["title", "created_at"] = "title"

class DocumentBase(BaseModel):
    """Base model for student documents"""
    title: str
    academic_session: str
    document_type: DocumentType

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "owner_id": "00000000-0000-0000-0000-000000000001",
                "title": "First Term Report Card",
                "academic_session": "2025/2026",
                "document_type": "RESULT",

            }
        }
    )


class DocumentCreate(DocumentBase):
    """Used for creating new student documents"""
    pass


class DocumentUpdate(BaseModel):
    """Used for updating student documents"""
    title: str
    document_type: DocumentType

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "title": "Second Term Report Card",
                "document_type": "RESULT",
            }
        }
    )


class DocumentResponse(DocumentBase):
    """Response model for student documents"""
    document_s3_key: str |None = None


class DocumentAudit(BaseModel):
    """Response model for student documents audit"""
    id: UUID
    owner_id: UUID
    document_s3_key: str | None = None
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None
