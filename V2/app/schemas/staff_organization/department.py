from ..common_imports import *
from ..shared_models import *


class DepartmentFilterParams(BaseFilterParams):
    name: Optional[str] = None
    description: Optional[str] = None
    order_by: Literal["name", "created_at"] = "name"


class StaffDepartmentBase(BaseModel):
    """Base model for staff departments"""
    name: str
    description: str
    manager_id: UUID | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
            "example": {
                "name": "Academic Affairs",
                "description": "Manages academic programs and curriculum",
                "manager_id": "00000000-0000-0000-0000-000000000000"
            }
        }
    )


class StaffDepartmentCreate(StaffDepartmentBase):
    """Used for creating new staff departments"""
    pass


class StaffDepartmentUpdate(StaffDepartmentBase):
    """Used for updating staff departments"""
    pass


class StaffDepartmentResponse(StaffDepartmentBase):
    """Response model for staff departments"""
    pass


class StaffDepartmentInDB(StaffDepartmentBase):
    """Represents stored staff departments"""
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
        extra="forbid",
        json_schema_extra = {
            "example": {
                "id": "00000000-0000-0000-0000-000000000000",
                "name": "Academic Affairs",
                "description": "Manages academic programs and curriculum",
                "manager_id": "00000000-0000-0000-0000-000000000000",
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
    )