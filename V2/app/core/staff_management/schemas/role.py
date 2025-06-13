from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *



class RolesFilterParams(BaseFilterParams):
    name: Optional[str] = None
    order_by: Literal["name", "created_at"] = "name"


class StaffRoleBase(BaseModel):
    """Base model for staff roles"""
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

class StaffRoleCreate(StaffRoleBase):
    """Used for creating new staff roles"""
    pass


class StaffRoleUpdate(StaffRoleBase):
    """Used for updating staff roles"""
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


class StaffRoleResponse(StaffRoleBase):
    """Response model for staff roles"""
    pass


class StaffRoleAudit(BaseModel):
    """Audit information staff role entities"""

    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None


class StaffRoleInDB:
    """Represents stored staff roles"""
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

