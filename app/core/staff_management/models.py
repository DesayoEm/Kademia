from app.core.shared.models.common_imports import *
from app.core.shared.models.mixins import AuditMixins, TimeStampMixins, ArchiveMixins
from app.core.shared.models.enums import ValidityType

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
    staff_members: Mapped[List["Staff"]] = relationship(back_populates='department',
                    primaryjoin="Staff.department_id == StaffDepartment.id")


    __table_args__ = (
        Index('idx_department_manager', 'manager_id'),
        Index('idx_staff_department_name', 'name'),
    )


class StaffTitle(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """Represents a title assigned to a staff member."""

    __tablename__ = 'staff_titles'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(500))

    # Relationships
    staff_members: Mapped[List["Staff"]] = relationship(back_populates='title',
            primaryjoin="Staff.title_id == StaffTitle.id")

    __table_args__ = (
        Index('idx_title_name', 'name'),
        Index('idx_title_description', 'description'),
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
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    validity_type: Mapped[ValidityType] = mapped_column(Enum(ValidityType, name='validitytype'),
                                    default=ValidityType.Temporary)
    valid_until: Mapped[str] = mapped_column(Text, nullable=False)
    is_expired: Mapped[bool] = mapped_column(Boolean, default=False)


    # Relationships
    educator: Mapped['Educator'] = relationship(
        'Educator', back_populates='qualifications',
        foreign_keys="[EducatorQualification.educator_id]", passive_deletes=True
    )

    __table_args__ = (
        UniqueConstraint('educator_id', 'name', name='uq_educator_qualification_name'),
        Index('idx_educator', 'educator_id'),
        Index('idx_qualification_name', 'name'),
    )


from app.core.identity.models.staff import Staff, Educator