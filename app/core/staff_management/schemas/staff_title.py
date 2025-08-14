from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.shared_models import *


class StaffTitleFilterParams(BaseFilterParams):
    name: Optional[str] = None
    order_by: Literal["name", "created_at"] = "name"


class StaffTitleBase(BaseModel):
    """Base model for staff titles"""
    name: str
    description: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        json_schema_extra = {
        "example": {
            "name": "Head of Department",
            "description": "Manages departmental operations and staff"
        }
    }
    )

class StaffTitleCreate(StaffTitleBase):
    """Used for creating new staff titles"""
    pass


class StaffTitleUpdate(StaffTitleBase):
    """Used for updating staff titles"""
    name: str | None = None
    description: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        json_schema_extra={
            "example": {
                "name": "Biology Teacher",
                "description": "Teaches biology"
            }
        }
    )


class StaffTitleResponse(StaffTitleBase):
    """Response model for staff titles"""
    pass


class StaffTitleAudit(BaseModel):
    """Audit information staff title entities"""

    id: UUID
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None


class StaffTitleInDB:
    """Represents stored staff titles"""
    id: UUID
    name: str
    description: str
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None

