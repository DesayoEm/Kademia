from ..common_imports import *
from ..shared_models import *
from ..enums import UserType, StaffType, StaffAvailability, EmploymentStatus
from .base import UserBase, ProfileInDb

class StaffFilterParams(BaseFilterParams):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    order_by: Literal["last_name", "created_at"] = "last_name"

class StaffEnumsRequest(BaseModel):
    user_type: UserType
    staff_type: StaffType
    staff_availability: StaffAvailability
    status: EmploymentStatus
    
class StaffBase(UserBase):
    """Base model for staff"""
    user_type: UserType
    status: EmploymentStatus
    staff_type: StaffType
    email_address: str
    address: str
    phone: str
    department_id: UUID
    role_id: UUID
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
            "user_type": "STAFF",
            "status": "ACTIVE",
            "staff_type": "Educator",
            "email_address": "aina.folu@example.com",
            "address": "456 Allen Avenue, Lagos",
            "phone": "+2348056794345",
            "department_id": "00000000-0000-0000-0000-000000000001",
            "role_id": "00000000-0000-0000-0000-000000000002",
            "date_joined": "2024-01-15",
        }
    })


class StaffCreate(StaffBase):
    """Used for creating new staff"""


class StaffUpdate(BaseModel):
    """Used for updating staff"""
    date_left: date | None = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "first_name": "Silver",
                "last_name": "Kincaid",
                "gender": "FEMALE",
                # Staff specific fields
                "user_type": "STAFF",
                "status": "ACTIVE",
                "staff_type": "Admin",
                "email_address": "aina.kincaid@example.com",
                "address": "456 Allen Avenue, Lagos",
                "phone": "+2348056794506",
                "department_id": "00000000-0000-0000-0000-000000000001",
                "role_id": "00000000-0000-0000-0000-000000000002",
                "date_joined": "2024-01-15",
                "date_left": None
            }
        })


class StaffResponse(StaffBase):
    """Response model for staff"""
    pass


class StaffInDB(StaffBase, ProfileInDb):
    """Represents stored staff"""

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
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
            "password_hash": "$2b$12$LQV3c1yqBWVHxk",
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
    })