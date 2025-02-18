from ..common_imports import *
from ..enums import AccessLevel, UserType, StudentStatus
from .base import ProfileBase, ProfileInDb


class StudentBase(ProfileBase):
    """Base model for students"""
    student_id: str
    user_type: UserType = UserType.STUDENT
    access_level: AccessLevel = AccessLevel.USER
    status: StudentStatus = StudentStatus.ENROLLED
    date_of_birth: date
    image_url: str | None = None
    class_id: UUID
    level_id: UUID
    department_id: UUID
    parent_id: UUID
    is_repeating: bool = False
    admission_date: date
    date_left: date | None = None
    graduation_date: date | None = None

    class Config:
        from_attributes = True

    json_schema_extra = {
        "example": {
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
            "parent_id": "00000000-0000-0000-0000-000000000004",
            "is_repeating": False,
            "admission_date": "2023-09-01",
            "date_left": None,
            "graduation_date": None
        }
    }


class StudentCreate(StudentBase):
    """Used for creating new students"""
    pass


class StudentUpdate(BaseModel):
    """Used for updating students"""
    pass


class StudentResponse(StudentBase):
    """Response model for students"""
    pass


class StudentInDB(StudentBase, ProfileInDb):
    """Represents stored students"""

    json_schema_extra = {
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
            "parent_id": "00000000-0000-0000-0000-000000000004",
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