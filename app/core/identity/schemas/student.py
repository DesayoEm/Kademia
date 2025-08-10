from ...shared.schemas.common_imports import *
from .base import UserBase, ProfileInDb
from ...shared.schemas.shared_models import *
from ...shared.schemas.enums import UserType, AccessLevel, StudentStatus


class StudentFilterParams(BaseFilterParams):
    full_name: str | None = None
    student_id: str | None = None
    session_start_year: int | None = None
    ward_id: UUID | None = None
    level_id: UUID | None = None
    class_id: UUID | None = None
    department_id: UUID | None = None
    is_graduated: bool | None = None
    graduation_year: str | None = None
    order_by: Literal["full_name", "student_id"] = "full_name"


class StudentBase(UserBase):
    """Base model for students"""
    session_start_year: int
    date_of_birth: date



class StudentCreate(StudentBase):
    """Used for creating new students"""
    date_of_birth: date
    level_id: UUID
    guardian_id: UUID



    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "first_name": "Omotara",
                "last_name": "Johnson",
                "gender": "FEMALE",
                "guardian_id": "00000000-0000-0000-0000-000000000004",
                "date_of_birth": "2010-05-15",
                "level_id": "00000000-0000-0000-0000-000000000002",
                "session_start_year": "2025",
            }
        })


class StudentUpdate(StudentBase):
    """Used for updating students"""

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
                "first_name": "Omotara",
                "last_name": "Johnson",
                "gender": "FEMALE",
                "date_of_birth": "2010-05-15",
                "session_start_year": "2025",
            }
        })

class StudentResponse(StudentCreate):
    """Response model for students"""

    student_id: str
    department_id: UUID | None = None
    class_id: UUID | None = None
    date_left: date | None = None
    is_graduated: bool
    graduation_year: str | None = None


class StudentAudit(BaseModel):
    id: UUID | None = None
    access_level: AccessLevel
    status: StudentStatus
    user_type: UserType
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

