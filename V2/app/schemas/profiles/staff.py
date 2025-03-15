from ..common_imports import *
from ..shared_models import *
from ..enums import AccessLevel, UserType, StaffType, StaffAvailability, EmploymentStatus
from .base import ProfileBase, ProfileInDb

class StaffFilterParams(BaseFilterParams):
    name: Optional[str] = None
    description: Optional[str] = None
    order_by: Literal["name", "created_at"] = "name"

class StaffEnumsRequest(BaseModel):
    access_level: AccessLevel
    user_type: UserType
    staff_type: StaffType
    staff_availability: StaffAvailability
    employment_status: EmploymentStatus
    
class StaffBase(ProfileBase):
    """Base model for staff"""
    access_level: AccessLevel
    user_type: UserType
    status: EmploymentStatus
    availability: StaffAvailability
    staff_type: StaffType
    image_url: str
    email_address: str
    address: str
    phone: str
    department_id: UUID
    role_id: UUID
    date_joined: date
    date_left: date | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
            "first_name": "Aina",
            "last_name": "Folu",
            "gender": "FEMALE",
            # Staff specific fields
            "access_level": "ADMIN",
            "user_type": "STAFF",
            "status": "ACTIVE",
            "availability": "AVAILABLE",
            "staff_type": "EDUCATOR",
            "image_url": "https://example.com/images/jane-doe.jpg",
            "email_address": "aina.folu@example.com",
            "address": "456 Allen Avenue, Lagos",
            "phone": "08087654321",
            "department_id": "00000000-0000-0000-0000-000000000001",
            "role_id": "00000000-0000-0000-0000-000000000002",
            "date_joined": "2024-01-15",
            "date_left": None
        }
    })


class StaffCreate(StaffBase):
    """Used for creating new staff"""
    pass


class StaffUpdate(BaseModel):
    """Used for updating staff"""
    pass


class StaffResponse(StaffBase):
    """Response model for staff"""
    pass


class StaffInDB(StaffBase, ProfileInDb):
    """Represents stored staff"""

    json_schema_extra = {
        "example": {
            #Base Profile fields
            "first_name": "Aina",
            "last_name": "Folu",
            "gender": "FEMALE",
            #Staff specific fields
            "access_level": "ADMIN",
            "user_type": "STAFF",
            "status": "ACTIVE",
            "availability": "AVAILABLE",
            "staff_type": "EDUCATOR",
            "image_url": "https://example.com/images/jane-doe.jpg",
            "email_address": "aina.folu@example.com",
            "address": "456 Allen Avenue, Lagos",
            "phone": "08087654321",
            "department_id": "00000000-0000-0000-0000-000000000001",
            "role_id": "00000000-0000-0000-0000-000000000002",
            "date_joined": "2024-01-15",
            "date_left": None,
            #ProfileInDb fields
            "id": "00000000-0000-0000-0000-000000000000",
            "password_hash": "$2b$12$LQV3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKxcqII5K8Ly.Nm",
            "created_at": "2024-02-17T12:00:00Z",
            "created_by": "00000000-0000-0000-0000-000000000001",
            "last_login": "2024-02-17T14:30:00Z",
            "deletion_eligible": False,
            "last_modified_at": "2024-02-17T12:00:00Z",
            "last_modified_by": "00000000-0000-0000-0000-000000000001",
            "is_archived": False,
            "archived_at": None,
            "archived_by": None,
            "archive_reason": None
        }
    }