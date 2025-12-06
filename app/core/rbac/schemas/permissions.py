from uuid import UUID
from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.enums import Action, Resource
from app.core.shared.schemas.shared_models import *


class PermissionFilterParams(BaseFilterParams):
    name: str | None = None
    resource: Resource | None = None
    action: Action | None = None


class PermissionBase(BaseModel):
    """Base model for permissions"""

    resource: Resource | None
    action: Action | None
    description: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "resource": "SUBJECTS",
                "action": "READ",
                "description": "educator permission",
            }
        },
    )


class PermissionCreate(PermissionBase):
    """For creating new Permissions"""

    pass


class PermissionResponse(PermissionBase):
    """Response model for Permissions"""

    name: str | None = None


class PermissionUpdate(PermissionBase):
    """Response model for Permissions"""

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "resource": "STUDENT",
                "action": "READ",
                "description": "educator permission",
            }
        },
    )


class PermissionAudit(PermissionBase):
    """Response model for Permissions"""

    id: UUID
    changed_at: datetime
    changed_by_id: UUID
