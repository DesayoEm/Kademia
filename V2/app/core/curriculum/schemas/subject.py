from V2.app.core.shared.schemas.common_imports import *
from V2.app.core.shared.schemas.shared_models import *

class SubjectFilterParams(BaseFilterParams):
    name: str|None = None
    order_by: Literal["name", "created_at"] = "name"

class SubjectBase(BaseModel):
    """Base model for subjects"""
    name: str
    department_id: UUID|None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
            "name": "Mathematics",
            "department_id": "00000000-0000-0000-0000-000000000001",

        }
        }
    )

class SubjectCreate(SubjectBase):
    """For creating new subjects"""
    pass


class SubjectUpdate(SubjectBase):
    """For updating subjects"""
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "name": "Advanced Biology",
                "department_id": "00000000-0000-0000-0000-000000000001"
            }
        }
    )

class SubjectResponse(SubjectBase):
    """Response model for subjects"""
    pass

