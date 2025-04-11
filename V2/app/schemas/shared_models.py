from pydantic import BaseModel, Field
from typing import Literal
from .common_imports import UUID, ConfigDict
from .enums import ArchiveReason, ExportFormat


class BaseFilterParams(BaseModel):
    limit: int = Field(25, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: str = "created_at"
    order_dir: Literal["asc", "desc"] = "asc"

class ArchiveRequest(BaseModel):
    reason: ArchiveReason

class ExportRequest(BaseModel):
    entity_type: str
    entity_id: UUID
    export_format: ExportFormat

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "entity_type": "StaffRole",
                "entity_id": "854d3006-8c13-49d8-afce-2f85b14064da",
                "export_format": "pdf"

            }
        }
    )
