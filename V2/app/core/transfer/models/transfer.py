from V2.app.core.shared.models.common_imports import *
from V2.app.core.shared.models.mixins import AuditMixins, TimeStampMixins, ArchiveMixins
from V2.app.core.shared.models.enums import ApprovalStatus

class ClassTransfer(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents a student's transfer between classes, including the reason, approval status, and status updates.
    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'class_transfers'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
                        ondelete='CASCADE',name='fk_student_department_transfers_students_student_id')
                    )
    academic_year: Mapped[int] = mapped_column(Integer)
    previous_class_id: Mapped[UUID] = mapped_column(ForeignKey('classes.id',
                        ondelete='RESTRICT', name='fk_student_department_transfers_classes_previous_class')
                    )
    new_class_id: Mapped[UUID] = mapped_column(ForeignKey('classes.id',
                        ondelete='RESTRICT', name='fk_student_department_transfers_classes_new_class')
                    )
    reason: Mapped[str] = mapped_column(String(500))
    status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus, name='approvalstatus'), default=ApprovalStatus.PENDING)
    status_updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id',
                        ondelete='RESTRICT',name='fk_student_department_transfers_staff_status_updated_by'),nullable=True
                    )
    status_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    transferred_student: Mapped['Student'] = relationship(back_populates='class_transfers', foreign_keys='[ClassTransfer.student_id]',
                         passive_deletes=True)
    previous_class: Mapped['Classes'] = relationship(foreign_keys='[ClassTransfer.previous_class_id]')
    new_class: Mapped['Classes'] = relationship(foreign_keys='[ClassTransfer.new_class_id]')
    status_changer: Mapped['Staff'] = relationship(foreign_keys='[ClassTransfer.status_updated_by]')

    __table_args__ = (
        Index('idx_class_transfer_status', 'status'),
        Index('idx_student_class_transfer_status', 'student_id', 'status'),
        Index('idx_student_class_transfer_academic_year', 'student_id', 'academic_year'),
        Index('idx_previous_class', 'previous_class_id'),
        Index('idx_new_class', 'new_class_id'),
    )

    def __repr__(self) -> str:
        return f"student {self.student_id} transfer from {self.previous_class_id} to {self.new_class_id} in {self.academic_year}\
        was actioned by {self.status_updated_by}"


class StudentDepartmentTransfer(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents a student's transfer between departments including the reason,approval status, and status updates.
    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'student_department_transfers'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
                    ondelete='CASCADE',name='fk_student_department_transfers_students_student_id'))

    academic_year: Mapped[int] = mapped_column(Integer)
    previous_level_id: Mapped[UUID] = mapped_column(ForeignKey('academic_levels.id',
                    ondelete='RESTRICT', name='fk_student_department_transfers_academic_levels_previous_level')
                                                    )
    new_level_id: Mapped[UUID] = mapped_column(ForeignKey('academic_levels.id',
                    ondelete='RESTRICT',name='fk_student_department_transfers_academic_levels_new_level')
                                               )
    previous_class_id: Mapped[UUID] = mapped_column(ForeignKey('classes.id',
                    ondelete='RESTRICT', name='fk_student_department_transfers_classes_previous_class')
                                                    )
    new_class_id: Mapped[UUID] = mapped_column(ForeignKey('classes.id',
                    ondelete='RESTRICT', name='fk_student_department_transfers_classes_new_class')
                                               )
    previous_department_id: Mapped[UUID] = mapped_column(
        ForeignKey('student_departments.id',
                    ondelete='RESTRICT', name='fk_student_transfers_previous_department')
    )
    new_department_id: Mapped[UUID] = mapped_column(ForeignKey('student_departments.id',
                    ondelete='RESTRICT',name='fk_student_transfers_new_department')
                                                    )
    reason: Mapped[str] = mapped_column(String(500))
    status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus, name='approvalstatus'), default=ApprovalStatus.PENDING)
    status_updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id',
                    ondelete='RESTRICT',name='fk_student_department_transfers_staff_status_updated_by'),nullable=True
                                                    )
    status_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    transferred_student: Mapped['Student'] = relationship(back_populates='department_transfers', foreign_keys='[StudentDepartmentTransfer.student_id]',
                         passive_deletes=True)
    former_dept: Mapped['StudentDepartment'] = relationship(foreign_keys='[StudentDepartmentTransfer.previous_department_id]')
    new_dept: Mapped['StudentDepartment'] = relationship(foreign_keys='[StudentDepartmentTransfer.new_department_id]')
    former_class_rel: Mapped['Classes'] = relationship(foreign_keys='[StudentDepartmentTransfer.previous_class_id]')
    new_class_rel: Mapped['Classes'] = relationship('Classes', foreign_keys='[StudentDepartmentTransfer.new_class_id]')
    previous_level_rel: Mapped['AcademicLevel'] = relationship(foreign_keys='[StudentDepartmentTransfer.previous_level_id]')
    new_level_rel: Mapped['AcademicLevel'] = relationship('AcademicLevel', foreign_keys='[StudentDepartmentTransfer.new_level_id]')
    status_changer: Mapped['Staff'] = relationship(foreign_keys='[StudentDepartmentTransfer.status_updated_by]')

    __table_args__ = (
        Index('idx_dept_transfer_status', 'status'),
        Index('idx_student_dept_transfer_status', 'student_id', 'status'),
        Index('idx_student_dept_transfer_academic_year', 'student_id', 'academic_year'),
        Index('idx_previous_department_id', 'previous_department_id'),
        Index('idx_new_department_id', 'new_department_id'),
    )

    def __repr__(self) -> str:
        return f"student {self.student_id} transfer from {self.previous_department_id} to {self.new_department_id} in {self.academic_year}\
        was actioned by {self.status_updated_by}"


from V2.app.core.identity.models.student import Student
from V2.app.core.identity.models.staff import Staff
from V2.app.core.academic_structure.models.academic_structure import AcademicLevel, Classes, StudentDepartment