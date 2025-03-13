from pydantic import BaseModel, Field
from typing import Literal
from .enums import ArchiveReason


class BaseFilterParams(BaseModel):
    limit: int = Field(50, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: str = "created_at"
    order_dir: Literal["asc", "desc"] = "desc"

class ArchiveRequest(BaseModel):
    reason: ArchiveReason