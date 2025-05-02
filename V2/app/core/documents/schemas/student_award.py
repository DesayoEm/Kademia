
from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *


class AwardFilterParams(BaseFilterParams):
    title: str|None = None
    session_year: str|None = None


    order_by: Literal["title", "created_at"] = "title"


class AwardBase(BaseModel):
    """Base model for student awards"""
    owner_id: UUID
    title: str
    description: str|None = None
    session_year: str


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "owner_id": "00000000-0000-0000-0000-000000000001",
                "title": "Outstanding Academic Achievement",
                "description": "Awarded for maintaining highest Math Score in the class",
                "session_year": "2025/2026",

            }
        }
    )


class AwardUpdate(BaseModel):
    """Used for updating student awards"""
    title: str | None = None
    description: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "title": "Outstanding Academic Achievement",
                "description": "Awarded for maintaining highest Math Score in the class"

            }
        }
    )


class AwardCreate(AwardBase):
    """Used for creating new student awards"""
    pass


class AwardResponse(AwardBase):
    """Response model for student awards"""
    file_url: str|None = None
