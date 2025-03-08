from ..common_imports import *
from ..enums import ArchiveReason
from ..shared_models import *


class QualificationFilterParams(BaseFilterParams):
    name: Optional[str] = None
    educator_id: Optional[UUID] = None
    order_by: Literal["name", "created_at"] = "name"


class QualificationBase(BaseModel):
    """Base model for educator qualifications"""
    educator_id: UUID
    name: str
    description: str | None = None


    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "educator_id": "00000000-0000-0000-0000-000000000001",
                "name": "Master of Science in Mathematics",
                "description": "Advanced degree in pure mathematics"
            }
        }
    )

class QualificationCreate(QualificationBase):
    """Used for creating new educator qualifications"""
    pass


class QualificationUpdate(BaseModel):
    """Used for updating educator qualifications"""
    name: str
    description: str | None


class QualificationResponse(QualificationBase):
    """Response model for educator qualifications"""
    pass


class QualificationInDB(QualificationBase):
    """Represents stored educator qualifications"""
    id: UUID
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "id": "00000000-0000-0000-0000-000000000000",
            "educator_id": "00000000-0000-0000-0000-000000000001",
            "name": "Master of Science in Mathematics",
            "description": "Advanced degree in pure mathematics",
            "created_at": "2024-02-17T12:00:00Z",
            "created_by": "00000000-0000-0000-0000-000000000000",
            "last_modified_at": "2024-02-17T12:00:00Z",
            "last_modified_by": "00000000-0000-0000-0000-000000000000",
            "is_archived": False,
            "archived_at": None,
            "archived_by": None,
            "archive_reason": None
            }

    )