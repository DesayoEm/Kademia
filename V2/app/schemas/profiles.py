from .common_imports import *
from .enums import Gender, AccessLevel, StaffType, UserType
from .validators import (validate_phone, validate_name,)


class DeleteBase(BaseModel):
    """Base model for storing deletion details"""
    is_soft_deleted: bool = False
    deleted_at: datetime | None = None
    deleted_by: UUID | None = None
    deletion_reason: str | None = None
    deletion_eligible: bool = False

    class Config:
        from_attributes = True

    

class Activity(BaseModel):
    is_active: bool
    last_login: datetime | None = None

    class Config:
        from_attributes = True
    


class ProfileBase(BaseModel):
    """Base model for creating new user"""
    id: UUID | None = None
    first_name: str
    last_name: str
    gender: Gender

    class Config:
        from_attributes = True


    @field_validator('first_name', 'last_name')
    def validate_first_and_last_name(cls, value):
        return validate_name(value)



class Profile(ProfileBase):
    """Complete user base model with system-generated fields."""
    #Audit
    created_at: datetime | None = None
    created_by: UUID | None = None
    last_modified_at: datetime | None = None
    last_modified_by: UUID | None = None

    class Config:
        from_attributes = True


class UpdateStudent(ProfileBase):
    """Model for updating existing student information."""
    image_url: str | None = Field(max_length=200)
    student_id: str = Field(max_length=20)
    class_id: UUID
    department_id: UUID
    parent_id: UUID
    admission_date: date
    leaving_date: date | None = None
    is_graduated: bool = Field(default=False)
    graduation_date: date | None = None
    is_enrolled: bool = Field(default=True)


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "first_name": "Lara",
                "last_name": "George",
                "image_url": "path_to_img",
                "gender": "Female",
                "date_of_birth": "2023-09-01",
                "student_id": "STU2",
                "class_id": "00000000-0000-0000-0000-000000000001",
                "department_id": "00000000-0000-0000-0000-000000000001",
                "parent_id": "00000000-0000-0000-0000-000000000001",
                "admission_date": "2023-09-01",
                "leaving_date": None,
                "is_graduated": False,
                "graduation_date": None,
                "is_enrolled": True
            }
        }


class NewStudent(UpdateStudent):
    """Full student model for initial creation"""
    password_hash: str
    date_of_birth: date

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                'password_hash': 'njeeeoi',
                "first_name": "Lara",
                "last_name": "George",
                "image_url": "path_to_img",
                "gender": "F",
                "date_of_birth": "2023-09-01",
                "student_id": "STU2",
                "class_id": "00000000-0000-0000-0000-000000000001",
                "department_id": "00000000-0000-0000-0000-000000000001",
                "parent_id": "00000000-0000-0000-0000-000000000001",
                "admission_date": "2023-09-01",
                "leaving_date": None,
                "is_graduated": False,
                "graduation_date": None,
                "is_enrolled": True
            }
        }


class Student(UpdateStudent, DeleteBase, Activity):
    """Full student profile"""
    date_of_birth: date
    

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "first_name": "Lara",
                "last_name": "George",
                "gender": "Female",
                "date_of_birth": "2023-09-01",
                "student_id": "STU2",
                "class_id": "5fd8c523-bc62-4b5d-a2f3-123456789abc",
                "department_id": "6fd8c523-bc62-4b5d-a2f3-123456789def",
                "parent_id": "7fd8c523-bc62-4b5d-a2f3-123456789ghi",
                "admission_date": "2023-09-01",
                "leaving_date": None,
                "is_graduated": False,
                "graduation_date": None,
                "is_enrolled": True,
                "is_active": True,
                "is_soft_deleted": False,
                "deleted_at":  None,
                "deleted_by": None,
                "deletion_reason": None

            }
        }


class UpdateParent(ProfileBase):
    """Model for updating existing parent information."""
    image_url: Optional[str] = Field(None, max_length=200)
    email_address: EmailStr = Field(max_length=255)
    address: str = Field(max_length=255)
    phone: str = Field(max_length=11)
    has_active_wards: bool = Field(default=True)

    @field_validator('phone')
    def validate_phone(cls, value):
        return validate_phone(value)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "first_name": "Kwame",
                "last_name": "John",
                "gender": "Male",
                "email_address": "kwame.john@example.com",
                "address": "123 Eric Moore",
                "phone": "08012345678"
            }
        }

class NewParent(UpdateParent):
    """Parent model for initial creation."""
    password_hash: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "first_name": "John",
                'password_hash': 'njeeeoi',
                "last_name": "Doe",
                "gender": "Male",
                "email_address": "john.doe@example.com",
                "address": "123 Main Street",
                "phone": "08012345678"
            }
        }



class UpdateStaff(ProfileBase):
    """Model for updating existing staff information."""
    image_url: Optional[str] = Field(None, max_length=200)
    email_address: EmailStr = Field(max_length=255)
    address: str = Field(max_length=500)
    phone: str = Field(max_length=11)
    department_id: UUID
    role_id: UUID
    date_joined: date
    date_left: date | None = None
    is_active: bool = Field(default=True)
    staff_type: StaffType

    @field_validator('phone')
    def validate_phone(cls, value):
        return validate_phone(value)

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "first_name": "Jane",
                "last_name": "Olabode",
                "gender": "Female",
                "email_address": "jane.olabode@example.com",
                "address": "456 Allen Avenue",
                "phone": "08087654321",
                "role_id": "6fd8c523-bc62-4b5d-a2f3-123456789def",
                "date_joined": "2023-01-15",
                "date_left": None,
                "staff_type": "Educator"
            }
        }


class NewStaff(UpdateStaff):
    """Full staff model for initial creation."""
    password_hash: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                'password_hash': 'njeeeoi',
                "first_name": "Jane",
                "last_name": "Olabode",
                "gender": "Female",
                "email_address": "jane.olabode@example.com",
                "address": "456 Allen Avenue",
                "phone": "08087654321",
                "role_id": "6fd8c523-bc62-4b5d-a2f3-123456789def",
                "date_joined": "2023-01-15",
                "date_left": None,
                "staff_type": "Educator"
            }
        }


