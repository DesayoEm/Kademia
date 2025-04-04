from ..common_imports import *
from ..shared_models import *
from ..enums import ValidityType


class QualificationFilterParams(BaseFilterParams):
    name: Optional[str] = None
    educator_id: Optional[UUID] = None
    order_by: Literal["name", "created_at"] = "name"


class QualificationBase(BaseModel):
    """Base model for educator qualifications"""
    educator_id: UUID
    name: str
    description: str | None = None
    validity_type : ValidityType
    valid_until: str



    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "educator_id": "00000000-0000-0000-0000-000000000001",
                "name": "Master of Science in Mathematics",
                "description": "Advanced degree in pure mathematics",
                "validity_type": "Lifetime",
                "valid_until": "Lifetime",
            }
        }
    )

class QualificationCreate(QualificationBase):
    """Used for creating new educator qualifications"""
    pass


class QualificationUpdate(BaseModel):
    """Used for updating educator qualifications"""
    name: str
    description: str | None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Master of Science in Geology",
                "description": "Advanced degree in stuff",
                "validity_type": "Temporary",
                "valid_until": "2029",
            }
        }
    )


class QualificationResponse(QualificationBase):
    """Response model for educator qualifications"""
    pass


class QualificationInDB:
    """Represents stored educator qualifications"""
    id: UUID
    educator_id: UUID
    name: str
    description: str | None = None
    validity_type : ValidityType
    valid_until: str
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None

