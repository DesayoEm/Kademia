from ..common_imports import *
from ..enums import Gender,  ArchiveReason


class ProfileBase(BaseModel):
    """Base model for creating new users"""
    first_name: str
    last_name: str
    gender: Gender


class ProfileInDb(BaseModel):
    """Represents stored profile data"""
    id: UUID
    password_hash:str
    created_at: datetime
    created_by: UUID
    last_login: datetime
    deletion_eligible: bool
    last_modified_at: datetime
    last_modified_by: UUID
    is_archived: bool
    archived_at: datetime | None = None
    archived_by: UUID | None = None
    archive_reason: ArchiveReason | None = None





