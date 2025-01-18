from common_imports import *
from enums import Gender, AccessLevel, StaffType
from validators import (
        validate_phone, validate_name, validate_admission_date
)

class UserBase(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
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

    class Config:
        from_attributes = True

    @field_validator('first_name', 'last_name')
    def validate_first_and_last_name(cls, value):
        return validate_name(value)


class Students(UserBase):
    id: UUID = Field(default_factory=uuid4)
    access_level: AccessLevel = Field(default=AccessLevel.USER)
    image_url: str = Field(max_length=200)
    student_id: str = Field(max_length=20)
    class_id: UUID
    department_id: UUID
    parent_id: UUID
    is_repeating: bool = Field(default=False)
    admission_date: date
    leaving_date: Optional[date] = None
    is_graduated: bool = Field(default=False)
    graduation_date: Optional[date] = None
    is_enrolled: bool = Field(default=True)

    @field_validator('admission_date')
    def validate_admission_date(cls, value):
        return validate_admission_date(value)



class Parents(UserBase):
    id: UUID = Field(default_factory=uuid4)
    access_level: AccessLevel = Field(default=AccessLevel.USER)
    image_url: Optional[str] = Field(None, max_length=200)
    email_address: EmailStr = Field(max_length=255)
    address: str = Field(max_length=255)
    phone: str = Field(max_length=11)
    has_active_wards: bool = Field(default=True)

    @field_validator('phone')
    def validate_phone(cls, value):
        return validate_phone(value)


class Staff(UserBase):
    id: UUID = Field(default_factory=uuid4)
    access_level: AccessLevel = Field(default=AccessLevel.ADMIN)
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

    @field_validator('phone')
    def validate_phone(cls, value):
        return validate_phone(value)


class Educator(Staff):
    pass

class Admin(Staff):
    pass

class Commercial(Staff):
    pass

class Management(Staff):
    pass

class Support(Staff):
    pass
