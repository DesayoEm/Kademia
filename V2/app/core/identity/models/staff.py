from .base import UserBase
from V2.app.core.shared.models.common_imports import *
from V2.app.core.shared.models.enums import AccessLevel, EmploymentStatus, UserType, StaffType, StaffAvailability


class Staff(UserBase):
    """
    Represents a staff member, including personal details, role, department, and employment status.
    Inherits from ProfileBase.
    """
    __tablename__ = 'staff'

    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel, name='accesslevel'), default=AccessLevel.READ)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType, name='usertype'), default=UserType.STAFF)
    status: Mapped[EmploymentStatus] = mapped_column(Enum(EmploymentStatus, name='employmentstatus'), default=EmploymentStatus.ACTIVE)
    availability: Mapped[StaffAvailability] = mapped_column(Enum(StaffAvailability, name='staffavailability'), default=StaffAvailability.AVAILABLE)
    staff_type: Mapped[StaffType] = mapped_column(Enum(StaffType, name='stafftype'))
    image_url: Mapped[str] = mapped_column(String(200), nullable = True)
    email_address: Mapped[str] = mapped_column(String(255), unique=True)
    address: Mapped[str] = mapped_column(String(500))
    phone: Mapped[str] = mapped_column(String(14), unique=True)
    department_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey('staff_departments.id', ondelete='SET NULL', name='fk_staff_staff_departments_department_id'),
        nullable=True
    )

    role_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey('staff_roles.id', ondelete='SET NULL', name='fk_staff_staff_roles_role_id'),
        nullable=True
    )
    date_joined: Mapped[date] = mapped_column(Date)
    date_left: Mapped[date] = mapped_column(Date, nullable=True)

    # Relationships
    department: Mapped["StaffDepartment"] = relationship(back_populates='staff_members', foreign_keys="[Staff.department_id]")
    role: Mapped["StaffRole"] = relationship(back_populates='staff_members', foreign_keys='[Staff.role_id]')
    access_changes: Mapped[List["AccessLevelChange"]] = relationship(
        "AccessLevelChange",
        back_populates='user',
        primaryjoin="Staff.id == AccessLevelChange.staff_id"
    )

    __table_args__ = (
        Index('idx_staff_name', 'first_name', 'last_name'),
        Index('idx_staff_department', 'department_id'),
        Index('idx_staff_role', 'role_id'),
        Index('idx_staff_phone', 'phone')
    )

    def __repr__(self) -> str:
        return f"Staff(name={self.first_name} {self.last_name}, role={self.role_id})"

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
        'polymorphic_on': staff_type
    }


class Educator(Staff):
    """
    Represents an educator, inheriting from Staff.
    Relationships:
        - qualifications
        - subjects: Subjects the educator is responsible for.
        - mentored_department (Departments): The department the educator mentors.
        - supervised_class (Classes): The class level the educator supervises.
    """
    __tablename__ = 'educators'

    id: Mapped[UUID] = mapped_column(
        ForeignKey('staff.id', ondelete='CASCADE', name='fk_educators_staff_id'),
        primary_key=True
    )

    __mapper_args__ = {
        'polymorphic_identity': 'Educator',
        'inherit_condition': (id == Staff.id)
    }

    qualifications: Mapped[List['EducatorQualification']] = relationship(back_populates='educator',
                    cascade="all, delete-orphan")
    subject_assignments: Mapped[List['SubjectEducator']] = relationship(back_populates='teacher')
    mentored_department: Mapped[List['StudentDepartment']] = relationship(back_populates='mentor')
    supervised_class: Mapped['Classes'] = relationship(back_populates='supervisor')

    def __repr__(self) -> str:
        return f"Educator(name={self.first_name} {self.last_name})"


class AdminStaff(Staff):
    """
    Represents an operations staff member, inheriting from Staff.
    """
    __tablename__ = 'admin_staff'

    id: Mapped[UUID] = mapped_column(
        ForeignKey('staff.id', ondelete='CASCADE', name='fk_operations_staff_id'),
        primary_key=True
    )

    __mapper_args__ = {
        'polymorphic_identity': 'Admin',
        'inherit_condition': (id == Staff.id)
    }

    def __repr__(self) -> str:
        return f"Operations staff(name={self.first_name} {self.last_name}, role_id={self.role_id})"


class SupportStaff(Staff):
    """
    Represents a support staff member, inheriting from Staff.
    """
    __tablename__ = 'support_staff'

    id: Mapped[UUID] = mapped_column(
        ForeignKey('staff.id', ondelete='CASCADE', name='fk_support_staff_id'),
        primary_key=True
    )

    __mapper_args__ = {
        'polymorphic_identity': 'Support',
        'inherit_condition': (id == Staff.id)
    }

    def __repr__(self) -> str:
        return f"Support staff(name={self.first_name} {self.last_name}, role_id={self.role_id})"


class System(Staff):
    """
    Represents the system, inheriting from Staff.
    """
    __tablename__ = 'system'

    id: Mapped[UUID] = mapped_column(
        ForeignKey('staff.id', ondelete='CASCADE', name='fk_system_staff_id'),
        primary_key=True
    )

    __mapper_args__ = {
        'polymorphic_identity': 'System',
        'inherit_condition': (id == Staff.id)
    }

    def __repr__(self) -> str:
        return f"System(name={self.first_name} {self.last_name}, role_id={self.role_id})"
