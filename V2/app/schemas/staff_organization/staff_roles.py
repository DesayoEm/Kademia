from ..common_imports import *
from ..enums import ArchiveReason


class StaffRoleBase(BaseModel):
    """Base model for staff roles"""
    name: str
    description: str

    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
            "name": "Head of Department",
            "description": "Manages departmental operations and staff"
        }
    }


class StaffRoleCreate(StaffRoleBase):
    """Used for creating new staff roles"""
    pass


class StaffRoleUpdate(StaffRoleBase):
    """Used for updating staff roles"""
    pass


class StaffRoleResponse(StaffRoleBase):
    """Response model for staff roles"""
    pass


class StaffRoleInDB(StaffRoleBase):
    """Represents stored staff roles"""
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
            "name": "Head of Department",
            "description": "Manages departmental operations and staff",
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