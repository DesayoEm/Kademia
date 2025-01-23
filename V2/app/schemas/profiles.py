from common_imports import *
from enums import Gender, AccessLevel, StaffType
from validators import (
        validate_phone, validate_name,
)

class NewUser(BaseModel):
    """
   Base model for creating new user
   """
    first_name: str
    last_name: str
    gender: Gender

    @field_validator('first_name', 'last_name')
    def validate_first_and_last_name(cls, value):
        return validate_name(value)


    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "first_name": "Lara",
                "last_name": "George",
                "gender": "Female"
            }
        }


class User(NewUser):
    """
    Complete user model with system-generated fields.
    Inherits `first_name`, `last_name`, and `gender` from `NewUser`.
    Adds audit and soft-delete attributes.
    """
    last_active_date: datetime | None = None
    deletion_eligible: bool = False

    #Audit
    created_at: datetime
    created_by: UUID
    last_modified_at: datetime
    last_modified_by: UUID

    #Soft delete
    is_soft_deleted: bool = False
    deleted_at: datetime | None = None
    deleted_by: UUID | None = None
    deletion_reason: str | None = None


class UpdateUser(NewUser):
    """
    Model for updating existing user information.
    Inherits basic user fields from `NewUser` and allows updates to the user information.
    """
    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Kehinde",
                "last_name": "George",
                "gender": "Male"
            }
        }

class UpdateStudent(NewUser):
    """Model for updating existing student information."""
    image_url: str = Field(max_length=200)
    student_id: str = Field(max_length=20)
    class_id: UUID
    department_id: UUID
    parent_id: UUID
    admission_date: date
    leaving_date: Optional[date] = None
    is_graduated: bool = Field(default=False)
    graduation_date: Optional[date] = None
    is_enrolled: bool = Field(default=True)


    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Kehinde",
                "last_name": "George",
                "gender": "Male",
                "student_id": "STU123456",
                "class_id": "5fd8c523-bc62-4b5d-a2f3-123456789abc",
                "department_id": "6fd8c523-bc62-4b5d-a2f3-123456789def",
                "parent_id": "7fd8c523-bc62-4b5d-a2f3-123456789ghi",
                "admission_date": "2023-09-01",
                "is_enrolled": True
            }
        }

class Students(UpdateStudent):
    """Full student model"""
    id: UUID = Field(default_factory=uuid4)
    access_level: AccessLevel = Field(default=AccessLevel.USER)
    is_repeating: bool = Field(default=False)


class UpdateParents(NewUser):
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
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "gender": "Male",
                "email_address": "john.doe@example.com",
                "address": "123 Main Street",
                "phone": "08012345678"
            }
        }

class Parents(UpdateParents):
    """
    Full parent model.
    """
    id: UUID = Field(default_factory=uuid4)
    access_level: AccessLevel = Field(default=AccessLevel.USER)



class UpdateStaff(User):
    """Model for updating existing staff information."""
    image_url: Optional[str] = Field(None, max_length=200)
    email_address: EmailStr = Field(max_length=255)
    address: str = Field(max_length=500)
    phone: str = Field(max_length=11)
    department_id: Optional[UUID] = None
    role_id: str
    date_joined: date
    date_left: Optional[date] = None
    is_active: bool = Field(default=True)
    staff_type: StaffType

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "first_name": "Jane",
                "last_name": "Smith",
                "gender": "Female",
                "email_address": "jane.smith@example.com",
                "address": "456 Allen Avenue",
                "phone": "08087654321",
                "role_id": "TEACHER",
                "date_joined": "2023-01-15",
                "staff_type": "Educator"
            }
        }


class Staff(UpdateStaff):
    """Full staff model."""
    id: UUID = Field(default_factory=uuid4)
    access_level: AccessLevel = Field(default=AccessLevel.ADMIN)


    @field_validator('phone')
    def validate_phone(cls, value):
        return validate_phone(value)


class Educator(Staff):
    """Model for Educators, inheriting all fields from Staff."""
    pass

class Operations(Staff):
    """Model for Operations staff, inheriting all fields from Staff."""
    pass

class Support(Staff):
    """Model for Support staff, inheriting all fields from Staff."""
    pass
