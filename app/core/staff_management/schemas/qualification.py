from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.shared_models import *
from app.core.shared.schemas.enums import ValidityType
from datetime import datetime


class QualificationFilterParams(BaseFilterParams):
    name: str | None = None
    educator_id: UUID | None = None
    is_expired: bool | None = None
    validity_type: ValidityType
    order_by: Literal["name", "created_at"] = "name"


class QualificationBase(BaseModel):
    """Base model for educator qualifications"""
    name: str
    description: str | None = None
    validity_type : ValidityType
    valid_until: str



    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Master of Science in Mathematics",
                "description": "Advanced degree in pure mathematics",
                "validity_type": "Temporary",
                "valid_until": "2026-06-01",
            }

        }
    )

class QualificationCreate(QualificationBase):
    """Used for creating new educator qualifications"""
    pass


class QualificationUpdate(BaseModel):
    """Used for updating educator qualifications"""
    name: str | None = None
    description: str | None = None
    validity_type: ValidityType | None = None
    valid_until: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Master of Science in Geology",
                "description": "Advanced degree in stuff",
                "validity_type": "Temporary",
                "valid_until": "2026-06-01",
            }
        }
    )


class QualificationResponse(QualificationBase):
    """Response model for educator qualifications"""
    pass


