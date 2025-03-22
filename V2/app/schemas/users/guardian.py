from ..common_imports import *
from .base import UserBase, ProfileInDb
from ..shared_models import *

class GuardianFilterParams(BaseFilterParams):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class GuardianBase(UserBase):
    """Base model for a Guardian"""
    email_address: str
    address: str
    phone: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "first_name": "Bola",
                "last_name": "Coker",
                "gender": "MALE",
                "email_address": "bola.coker@example.com",
                "address": "123 Akala Express Ibadan",
                "phone": "08012345678"
        }
        }
    )



class GuardianCreate(GuardianBase):
    """Used for creating a new  Guardian"""
    pass


class GuardianUpdate(GuardianBase):
    """Used for updating a Guardian"""
    pass


class GuardianResponse(GuardianBase):
    """Response model for a Guardian"""
    pass


class GuardiansInDB(GuardianBase, ProfileInDb):
    """Represents a stored Guardian"""

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
            #Base Profile fields
            "first_name": "Bola",
            "last_name": "Coker",
            "gender": "MALE",
            #Guardian specific fields
            "email_address": "bola.coker@example.com",
            "address": "123 Akala Express Ibadan",
            "phone": "08012345678",
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
    })