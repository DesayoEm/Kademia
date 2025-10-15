from .base import UserBase
from app.core.shared.models.common_imports import *
from app.core.shared.models.enums import StaffStatus, UserType, StaffType, StaffAvailability



class Staff(UserBase):
    __tablename__ = 'staff'

    current_role_id: Mapped[UUID] = mapped_column(ForeignKey('roles.id', ondelete='RESTRICT'), nullable=True)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType, name='usertype'), default=UserType.STAFF)
    staff_type: Mapped[StaffType] = mapped_column(Enum(StaffType, name='stafftype'))

    status: Mapped[StaffStatus] = mapped_column(Enum(StaffStatus, name='employmentstatus'), default=StaffStatus.ACTIVE)
    availability: Mapped[StaffAvailability] = mapped_column(Enum(StaffAvailability, name='staffavailability'), default=StaffAvailability.AVAILABLE)
    email_address: Mapped[str] = mapped_column(String(255), unique=True)
    address: Mapped[str] = mapped_column(String(500))
    phone: Mapped[str] = mapped_column(String(14), unique=True)
    department_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey('staff_departments.id', ondelete='SET NULL', name='fk_staff_staff_departments_department_id'),
        nullable=True
    )

    job_title_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey('staff_job_titles.id', ondelete='SET NULL', name='fk_staff_staff_job_titles_title_id'),
        nullable=True
    )
    date_joined: Mapped[date] = mapped_column(Date)
    date_left: Mapped[date] = mapped_column(Date, nullable=True)

    # Relationships
    department: Mapped["StaffDepartment"] = relationship(back_populates='staff_members', foreign_keys="[Staff.department_id]")
    title: Mapped["StaffJobTitle"] = relationship(back_populates='staff_members', foreign_keys='[Staff.job_title_id]')
    role: Mapped["Role"] = relationship(back_populates='staff_members',foreign_keys="[Staff.current_role_id]")

    role_changes: Mapped[List["RoleHistory"]] = relationship(
        "RoleHistory",
        back_populates="staff_member",
        primaryjoin="foreign(RoleHistory.staff_id) == Staff.id"
    )

    __table_args__ = (
        Index('idx_staff_name', 'first_name', 'last_name'),
        Index('idx_staff_department', 'department_id'),
        Index('idx_staff_job_title', 'job_title_id'),
        Index('idx_staff_phone', 'phone')
    )

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
    """Represents an admin staff member."""
    __tablename__ = 'admin_staff'

    id: Mapped[UUID] = mapped_column(
        ForeignKey('staff.id', ondelete='CASCADE', name='fk_operations_staff_id'),
        primary_key=True
    )

    __mapper_args__ = {
        'polymorphic_identity': 'Admin',
        'inherit_condition': (id == Staff.id)
    }


class SupportStaff(Staff):
    """Represents a support staff member."""
    __tablename__ = 'support_staff'

    id: Mapped[UUID] = mapped_column(
        ForeignKey('staff.id', ondelete='CASCADE', name='fk_support_staff_id'),
        primary_key=True
    )

    __mapper_args__ = {
        'polymorphic_identity': 'Support',
        'inherit_condition': (id == Staff.id)
    }



class System(Staff):
    """Represents the system, inheriting from Staff."""
    __tablename__ = 'system'

    id: Mapped[UUID] = mapped_column(
        ForeignKey('staff.id', ondelete='CASCADE', name='fk_system_staff_id'),
        primary_key=True
    )

    __mapper_args__ = {
        'polymorphic_identity': 'System',
        'inherit_condition': (id == Staff.id)
    }





from ...rbac.models import RoleHistory, Role
from app.core.staff_management.models import StaffDepartment, StaffJobTitle, EducatorQualification
from app.core.curriculum.models.curriculum import SubjectEducator
from app.core.academic_structure.models import StudentDepartment, Classes