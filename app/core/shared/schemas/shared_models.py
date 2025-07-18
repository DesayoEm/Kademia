from pydantic import BaseModel, Field
from typing import Literal
from .enums import ArchiveReason, ExportFormat


class BaseFilterParams(BaseModel):
    limit: int = Field(25, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: str = "created_at"
    order_dir: Literal["asc", "desc"] = "asc"

class ArchiveRequest(BaseModel):
    reason: ArchiveReason

class ExportRequest(BaseModel):
    export_format: ExportFormat

class UploadResponse(BaseModel):
    """Response model for successful uploads."""
    filename: str
    size: int
    file_type: str