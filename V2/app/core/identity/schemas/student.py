from ...shared.schemas.common_imports import *
from .base import UserBase, ProfileInDb
from ...shared.schemas.shared_models import *


class StudentFilterParams(BaseFilterParams):
    full_name: str | None = None
    student_id: str | None = None
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


class StudentInDB(StudentBase, ProfileInDb):
    """Represents stored students"""

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "example": {
            #Base Profile fields
            "first_name": "Omotara",
            "last_name": "Johnson",
            "gender": "FEMALE",
            #Student specific fields
            "student_id": "STU/23/24/0001",
            "user_type": "STUDENT",
            "access_level": "USER",
            "status": "ENROLLED",
            "date_of_birth": "2010-05-15",
            "image_url": "https://example.com/images/alice-johnson.jpg",
            "class_id": "00000000-0000-0000-0000-000000000001",
            "level_id": "00000000-0000-0000-0000-000000000002",
            "department_id": "00000000-0000-0000-0000-000000000003",
            "guardian_id": "00000000-0000-0000-0000-000000000004",
            "is_repeating": False,
            "admission_date": "2023-09-01",
            "date_left": None,
            "graduation_date": None,
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
    )