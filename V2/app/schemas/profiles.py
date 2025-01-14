from common_imports import *
from enums import Gender, AccessLevel, StaffType


class UserBase(BaseModel):
    first_name: str
    last_name: str
    gender: Gender
    last_active_date: datetime | None = None
    deletion_eligible: bool = False

    #Audit
    created_at: datetime
    created_by: UUID
    updated_at: datetime
    updated_by: UUID

    #Soft delete
    is_soft_deleted: bool = False
    deleted_at: datetime | None = None
    deleted_by: UUID | None = None
    deletion_reason: str | None = None

    class Config:
        from_attributes = True


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


class Parents(UserBase):
    id: UUID = Field(default_factory=uuid4)
    access_level: AccessLevel = Field(default=AccessLevel.USER)
    image_url: Optional[str] = Field(None, max_length=200)
    email_address: EmailStr = Field(max_length=255)
    address: str = Field(max_length=255)
    phone: str = Field(max_length=11)
    has_active_wards: bool = Field(default=True)



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


class Educator(Staff):
    pass

class Admin(Staff):
    pass



# def validate_year(year: int) -> int:
#     current_year = date.today().year
#     if year < 1900:
#         raise Exception()
#     if year > current_year:
#         raise Exception()
#     return year
#
#
# def validate_phone(phone: str) -> bool:
#     if not len(phone) == 11 or not phone.isdigit():
#         raise ValueError("Phone must be 11 digits")
#     return phone
#
# def validate_name(name: str, max_length: int = 30) -> bool:
#     if not name or len(name) > max_length:
#         raise ValueError(f"Name must be between 1 and {max_length} characters")
#     return name