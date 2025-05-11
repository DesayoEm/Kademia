from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *


class AcademicLevelFilterParams(BaseFilterParams):
    name: str | None = None
    order_by: Literal["display_order", "created_at"] = "order"

class AcademicLevelBase(BaseModel):
    """Base model for academic levels"""
    name: str
    description: str
    promotion_rank: int

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
    name: str | None = None
    description: str | None = None
    display_order: int | None = None
    promotion_rank: int | None = None

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
