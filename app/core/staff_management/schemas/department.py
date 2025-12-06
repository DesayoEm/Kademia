from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.shared_models import *


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
        json_schema_extra={
            "example": {
                "name": "Academic Affairs",
                "description": "Manages academic programs and curriculum",
            }
        },
    )


class StaffDepartmentCreate(StaffDepartmentBase):
    """Used for creating new staff departments"""

    pass


class StaffDepartmentUpdate(StaffDepartmentBase):
    """Used for updating staff departments"""

    name: str | None = None
    description: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "name": "Academic Affairs",
                "description": "Manages academic programs",
            }
        },
    )


class StaffDepartmentResponse(StaffDepartmentBase):
    """Response model for staff departments"""

    manager_id: UUID | None = None


class StaffDepartmentAudit(BaseModel):
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
