from ..common_imports import *
from ..shared_models import *


class AcademicLevelFilterParams(BaseFilterParams):
    name: Optional[str] = None
    description: Optional[str] = None
    order_by: Literal["order", "created_at"] = "order"

class AcademicLevelBase(BaseModel):
    """Base model for academic levels"""
    name: str
    description: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra = {
                "example": {
                    "name": "JSS1",
                    "description": "First Level in the Secondary School System"

                }
        }
    )


class AcademicLevelCreate(AcademicLevelBase):
    """For creating new academic levels"""

class AcademicLevelUpdate(AcademicLevelBase):
    """For updating academic levels"""
    order: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "name": "JSS1",
                "description": "First Level in the Secondary School System",
                "order":10

            }
        }
    )



class AcademicLevelResponse(AcademicLevelBase):
    """Response model for class levels"""
    order: int

class AcademicLevelInDB(AcademicLevelBase):
    """Represents stored class levels"""
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
