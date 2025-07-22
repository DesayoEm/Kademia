from ...shared.schemas.common_imports import *
from ...shared.schemas.shared_models import *
from ...shared.schemas.enums import StaffType, UserType, EmploymentStatus, StaffAvailability, AccessLevel
from .base import UserBase


class StaffFilterParams(BaseFilterParams):
    full_name: str | None = None
    staff_type: StaffType | None = None
    department_id: UUID | None = None
    role_id: UUID | None = None
    order_by: Literal["full_name", "created_at"] = "full_name"


class StaffBase(UserBase):
    """Base model for staff"""
    email_address: str
    address: str
    phone: str


class StaffCreate(StaffBase):
    """Used for creating new staff"""
    staff_type: StaffType
    date_joined: date

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "first_name": "Aina",
                "last_name": "Folu",
                "gender": "FEMALE",
                # Staff specific fields
                "staff_type": "Educator",
                "email_address": "aina.folu@example.com",
                "address": "456 Allen Avenue, Lagos",
                "phone": "+2348056794345",
                "date_joined": "2024-01-15",
            }
        })


class StaffUpdate(StaffBase):
    """Used for updating staff"""


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "first_name": "Silver",
                "last_name": "Kincaid",
                "gender": "FEMALE",


                "email_address": "aina.kincaid@example.com",
                "address": "456 Allen Avenue, Lagos",
                "phone": "+2348056794506",
            }
        })


class StaffResponse(StaffCreate):
    """Response model for staff"""
    staff_type: StaffType | None = None
    date_joined: date | None = None
    profile_s3_key: str | None = None
    department_id: UUID | None = None
    role_id: UUID | None = None


class StaffAudit(BaseModel):
    id: UUID | None = None
    access_level: AccessLevel
    user_type: UserType
    status: EmploymentStatus
    availability: StaffAvailability
    date_left: date | None = None
    created_at: datetime | None = None
    created_by: UUID
    last_modified_at: datetime | None = None
    last_modified_by: UUID
    last_login: datetime | None = None
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None
    deletion_eligible: bool


