from app.database.models.common_imports import *
from app.database.models.data_enums import StaffType, Gender, AccessLevel
from app.database.models.mixins import AuditMixins, SoftDeleteMixins, TimeStampMixins
from sqlalchemy.orm import declared_attr
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as SAUUID
import uuid


class ProfileBase(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __abstract__ = True

    profile_id: Mapped[UUID] =mapped_column(SAUUID, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    gender: Mapped[str] = mapped_column(Enum(Gender))
    last_active_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deletion_eligible: Mapped[bool] = mapped_column(Boolean, default=False)



class Students(ProfileBase):
    __tablename__ = 'students'

    id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), primary_key=True, default=uuid4)
    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel), default = AccessLevel.USER)
    image_url: Mapped[str] = mapped_column(String(200))
    student_id: Mapped[str] = mapped_column(String(20), unique=True)
    class_id: Mapped[UUID] =mapped_column(SAUUID(as_uuid=True), default=uuid.uuid4)
    department_id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), default=uuid.uuid4)
    parent_id: Mapped[UUID] =mapped_column(SAUUID(as_uuid=True), default=uuid.uuid4)
    is_repeating: Mapped[bool] = mapped_column(Boolean, default=False)
    admission_date: Mapped[date] = mapped_column(Date)
    leaving_date: Mapped[date] = mapped_column(Date, nullable=True)
    is_graduated: Mapped[bool] = mapped_column(Boolean, default=False)
    graduation_date: Mapped[date] = mapped_column(Date, nullable=True)
    is_enrolled: Mapped[bool] = mapped_column(Boolean, default=True)


    def __repr__(self) -> str:
        return f"Student(name={self.first_name} {self.last_name}, class={self.class_id})"


class Parents(ProfileBase):
    __tablename__ = 'parents'
    id: Mapped[UUID] = mapped_column(SAUUID(as_uuid=True), primary_key=True, default=uuid4)
    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel), default = AccessLevel.USER)
    image_url: Mapped[str] = mapped_column(String(200), nullable=True)
    email_address: Mapped[str] = mapped_column(String(255), unique=True)
    address: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(11), unique=True)
    has_active_wards: Mapped[bool] = mapped_column(Boolean, default=True)

    #Relationships
    wards = relationship('Students', back_populates='parent')

    __table_args__ = (
        Index('idx_parents_email', 'email_address'),
        Index('idx_parents_phone', 'phone'),
        Index('idx_parents_soft_deleted_at', 'soft_deleted_at'),
        Index('idx_parents_profile_id', 'profile_id')
    )

    def __repr__(self) -> str:
        return f"Parent(name={self.first_name} {self.last_name}, phone={self.phone})"


class Staff(ProfileBase):
    __tablename__ = 'staff'

    id: Mapped[UUID]  = mapped_column(SAUUID(as_uuid = True), primary_key= True, default = uuid4)
    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel), default = AccessLevel.ADMIN)
    image_url: Mapped[str] = mapped_column(String(200))
    email_address: Mapped[str] = mapped_column(String(255), unique=True)
    address: Mapped[str] = mapped_column(String(500))
    phone: Mapped[str] = mapped_column(String(11), unique=True)
    department_id: Mapped[Optional[UUID]] =mapped_column(SAUUID(as_uuid=True), default=uuid.uuid4)
    role_id: Mapped[UUID] =mapped_column(SAUUID(as_uuid=True), default=uuid.uuid4)
    date_joined: Mapped[date] = mapped_column(Date)
    date_left: Mapped[date] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default = True)
    staff_type: Mapped[StaffType] = mapped_column(Enum(StaffType))


    __table_args__ = (
        Index('idx_staff_soft_deleted_at', 'soft_deleted_at'),
        Index('idx_staff_department', 'department_id'),
        Index('idx_staff_role', 'role_id'),
        Index('idx_staff_type', 'staff_type'),
        Index('idx_staff_name', 'first_name', 'last_name'),
        Index('idx_staff_profile_id', 'profile_id')
    )

    def __repr__(self) -> str:
        return f"Staff(name={self.first_name} {self.last_name}, is_active={self.is_active})"


class Admin(Staff):
    __tablename__ = 'admin'

    id: Mapped[UUID] = mapped_column(primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
        'inherit_condition': (Staff.id == 'Admin.id'),
    }

    def __repr__(self) -> str:
        return f"Admin(name={self.first_name} {self.last_name}, role={self.role_id})"


class Educator(Staff):
    __tablename__ = 'educator'

    id: Mapped[UUID] = mapped_column(primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'educator',
        'inherit_condition': (id == Staff.id),
    }

    subjects_taken = relationship('EducatorSubjects', back_populates='educator')
    mentored_department = relationship("Departments", back_populates="mentor")
    mentored_class = relationship("Classes", back_populates="mentor")


class Management(Staff):
    __tablename__ = 'management'

    id: Mapped[UUID] = mapped_column(primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'management',
        'inherit_condition': (id == Staff.id),
    }

    def __repr__(self) -> str:
        return f"Management staff(name ={self.first_name} {self.last_name}, role_id={self.role_id})"


class Commercial(Staff):
    __tablename__ = 'commercial'

    id: Mapped[UUID] = mapped_column(primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'commercial',
        'inherit_condition': (id == Staff.id),
    }

    def __repr__(self) -> str:
        return f"Comms staff(name ={self.first_name} {self.last_name}, role_id={self.role_id})"


class Support(Staff):
    __tablename__ = 'support'

    id: Mapped[UUID] = mapped_column(primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'support',
        'inherit_condition': (id == Staff.id),
    }

    def __repr__(self) -> str:
        return f"Support staff(name ={self.first_name} {self.last_name}, role_id={self.role_id})"





