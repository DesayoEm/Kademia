from .common_imports import *
from .mixins import AuditMixins, ArchiveMixins, TimeStampMixins


class StaffDepartment(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents a staff department.
    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'staff_departments'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(500))
    manager_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id',
            ondelete='SET NULL', name='fk_staff_departments_staff_manager_id'),nullable=True
        )

    # Relationships
    manager: Mapped['Staff'] = relationship(foreign_keys='[StaffDepartment.manager_id]')
    staff: Mapped[List["Staff"]] = relationship(back_populates='department',
                    primaryjoin="Staff.department_id == StaffDepartment.id")


    __table_args__ = (
        Index('idx_department_manager', 'manager_id'),
        Index('idx_staff_department_name', 'name'),
    )


class StaffRole(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents a role assigned to a staff member, including the role name and description.
    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'staff_roles'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(500))

    # Relationships
    staff: Mapped[List["Staff"]] = relationship(back_populates='role',
            primaryjoin="Staff.role_id == StaffRole.id")

    __table_args__ = (
        Index('idx_role_name', 'name'),
        Index('idx_role_description', 'description'),
    )


class EducatorQualification(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents an educator's academic qualifications.
    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'educator_qualifications'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    educator_id: Mapped[UUID] = mapped_column(ForeignKey('educators.id',
            ondelete='CASCADE', name='fk_educator_qualifications_educators_educator_id')
        )
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    # Relationships
    educator: Mapped['Educator'] = relationship(
        'Educator', back_populates='qualifications',
        foreign_keys="[EducatorQualification.educator_id]"
    )

    __table_args__ = (
        Index('idx_educator', 'educator_id'),
        Index('idx_qualification_name', 'name'),
    )
