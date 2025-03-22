from ..common_imports import *
from ..enums import ArchiveReason, AccessLevel, UserType
from .base import UserBase, ProfileInDb


class GuardiansBase(UserBase):
    """Base model for a Guardian"""
    access_level: AccessLevel
    user_type: UserType
    image_url: str | None = None
    email_address: str
    address: str
    phone: str


    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
            "first_name": "Bola",
            "last_name": "Coker",
            "gender": "MALE",
            #Guardian specific fields
            "access_level": "USER",
            "image_url": "https://example.com/images/john-smith.jpg",
            "email_address": "bola.coker@example.com",
            "address": "123 Akala Express Ibadan",
            "phone": "08012345678"
        }
        }



class GuardianCreate(GuardiansBase):
    """Used for creating a new  Guardian"""
    pass


class GuardiansUpdate(BaseModel):
    """Used for updating a Guardian"""
    pass


class GuardiansResponse(GuardiansBase):
    """Response model for a Guardian"""
    pass


class GuardiansInDB(GuardiansBase, ProfileInDb):
    """Represents a stored Guardian"""


    json_schema_extra = {
        "example": {
            #Base Profile fields
            "first_name": "Bola",
            "last_name": "Coker",
            "gender": "MALE",
            #Guardian specific fields
            "access_level": "USER",
            "user_type": "Guardian",
            "image_url": "https://example.com/images/john-smith.jpg",
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
    }