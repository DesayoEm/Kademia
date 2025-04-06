from ..common_imports import *
from ..shared_models import *


class DepartmentFilterParams(BaseFilterParams):
    name: Optional[str] = None
    order_by: Literal["name", "created_at"] = "name"


class StaffDepartmentBase(BaseModel):
    """Base model for staff departments"""
    name: str
    description: str


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
            "example": {
                "name": "Academic Affairs",
                "description": "Manages academic programs and curriculum",
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


class StaffDepartmentInDB:
    """Represents stored staff departments"""
    id: UUID
    name: str
    description: str
    manager_id: UUID | None = None
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None


