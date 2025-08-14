from ...shared.schemas.common_imports import *
from .base import UserBase
from ...shared.schemas.enums import Title, UserType, UserRole
from ...shared.schemas.shared_models import *


class GuardianFilterParams(BaseFilterParams):
    full_name: str | None = None
    order_by: Literal["full_name", "created_at"] = "full_name"


class GuardianBase(UserBase):
    """Base model for a Guardian"""
    email_address: str
    address: str
    phone: str
    title: Title

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "title":"Ms",
                "first_name": "Bola",
                "last_name": "Coker",
                "gender": "MALE",
                "email_address": "bola.coker@example.com",
                "address": "123 Akala Express Ibadan",
                "phone": "+2348056794345"
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


class GuardianAudit(BaseModel):
    id: UUID | None = None
    current_role: UserRole
    user_type: UserType

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

