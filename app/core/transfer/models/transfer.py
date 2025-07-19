from app.core.shared.models.common_imports import *
from app.core.shared.models.mixins import AuditMixins, TimeStampMixins, ArchiveMixins
from app.core.shared.models.enums import ApprovalStatus


class DepartmentTransfer(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents a student's transfer between departments including the reason,approval status, and status updates.
    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'student_department_transfers'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
                    ondelete='CASCADE',name='fk_student_department_transfers_students_student_id'))

    academic_session: Mapped[str] = mapped_column(String(9))

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
    transferred_student: Mapped['Student'] = relationship(back_populates='department_transfers', foreign_keys='[DepartmentTransfer.student_id]',
                         passive_deletes=True)
    former_dept: Mapped['StudentDepartment'] = relationship(foreign_keys='[DepartmentTransfer.previous_department_id]')
    new_dept: Mapped['StudentDepartment'] = relationship(foreign_keys='[DepartmentTransfer.new_department_id]')
    status_changer: Mapped['Staff'] = relationship(foreign_keys='[DepartmentTransfer.status_updated_by]')

    __table_args__ = (
        Index('idx_dept_transfer_status', 'status'),
        Index('idx_student_dept_transfer_status', 'student_id', 'status'),
        Index('idx_student_dept_transfer_academic_session', 'student_id', 'academic_session'),
        Index('idx_previous_department_id', 'previous_department_id'),
        Index('idx_new_department_id', 'new_department_id'),
    )

    def __repr__(self) -> str:
        return f"student {self.student_id} transfer from {self.previous_department_id} to {self.new_department_id} in {self.academic_session}\
        was actioned by {self.status_updated_by}"


from app.core.identity.models.student import Student
from app.core.identity.models.staff import Staff
from app.core.academic_structure.models import AcademicLevel, Classes, StudentDepartment