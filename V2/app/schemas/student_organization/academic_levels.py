from ..common_imports import *
from ..shared_models import *


class AcademicLevelFilterParams(BaseFilterParams):
    name: Optional[str] = None
    description: Optional[str] = None
    order_by: Literal["order", "created_at"] = "order"


class AcademicLevelBase(BaseModel):
    """Base model for class levels"""
    name: str
    description: str
    order: int | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
                "example": {
                    "name": "JSS1",
                    "description": "First Level in the Secondary School System",
                    "order": 1
                }
        }
    )

class AcademicLevelUpdate(AcademicLevelBase):
    """Used for updating class levels"""
    pass



class AcademicLevelCreate(AcademicLevelBase):
    """Used for creating new class levels"""
    pass

class AcademicLevelResponse(AcademicLevelBase):
    """Response model for class levels"""
    pass

class AcademicLevelInDB(AcademicLevelBase):
    """Represents stored class levels"""
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
        extra="ignore",
        json_schema_extra = {
        "example": {
            "name": "JSS2",
            "description": "Second Level in the Secondary School System",
            "order": 1,
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