
from uuid import UUID
from app.core.shared.schemas.common_imports import *
from app.core.shared.schemas.shared_models import *
from app.core.shared.schemas.enums import UserRoleName


class RoleFilterParams(BaseFilterParams):
    name: UserRoleName | None = None


class RoleBase(BaseModel):
    """Base model for roles"""
    name: UserRoleName | None = None
    description: str
    rank: int


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "name": "EDUCATOR",
                "description": "educator",
                "rank": 2,
            }
        }
    )


class RoleCreate(RoleBase):
    """For creating new roles"""
    pass


class RoleResponse(RoleBase):
    """Response model for roles"""
    pass

class RoleUpdate(RoleBase):
    """Response model for roles"""
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "name": "EDUCATOR",
                "description": "educator with limited access",
                "rank": 3,
            }
        }
    )


class RoleAudit(RoleBase):
    """Response model for roles"""
    id: UUID
    changed_at: datetime
    changed_by_id: UUID


