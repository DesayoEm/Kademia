from V2.app.core.shared.models.common_imports import *
from V2.app.core.shared.models.mixins import AuditMixins, TimeStampMixins, ArchiveMixins
from V2.app.core.shared.models.enums import ApprovalStatus

class Repetition(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """Represents a student's repetition of a class"""
    __tablename__ = 'repetitions'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='CASCADE',name='fk_repetitions_students_student_id')
        )
    academic_session: Mapped[str] = mapped_column(String(9))
    previous_level_id: Mapped[UUID] = mapped_column(ForeignKey('academic_levels.id',
            ondelete='RESTRICT',name='fk_repetitions_academic_levels_previous_level')
        )
    new_level_id: Mapped[UUID] = mapped_column(ForeignKey('academic_levels.id',
            ondelete='RESTRICT',name='fk_repetitions_academic_levels_new_level')
        )
    previous_class_id: Mapped[UUID] = mapped_column(ForeignKey('classes.id',
            ondelete='RESTRICT',name='fk_repetitions_classes_previous_class')
        )
    new_class_id: Mapped[UUID] = mapped_column(ForeignKey('classes.id',
            ondelete='RESTRICT', name='fk_repetitions_classes_new_class')
        )
    reason: Mapped[str] = mapped_column(String(500))
    status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus, name='approvalstatus'), default=ApprovalStatus.PENDING)
    status_updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id',
            ondelete='RESTRICT',name='fk_repetitions_staff_status_updated_by'),nullable=True
        )
    status_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    repeating_student: Mapped['Student'] = relationship(back_populates='classes_repeated',
                        foreign_keys='[Repetition.student_id]', passive_deletes=True)
    previous_level: Mapped['AcademicLevel'] = relationship(foreign_keys='[Repetition.previous_level_id]')
    new_level:Mapped['AcademicLevel'] =  relationship( foreign_keys='[Repetition.new_level_id]')
    previous_class: Mapped['Classes'] = relationship(foreign_keys='[Repetition.previous_class_id]')
    new_class:Mapped['Classes'] =  relationship( foreign_keys='[Repetition.new_class_id]')
    status_updated_staff:Mapped['Staff'] =  relationship(foreign_keys='[Repetition.status_updated_by]')

    __table_args__ = (
        Index('idx_repetition_status', 'student_id', 'status'),
        Index('idx_repetition_academic_session', 'student_id', 'academic_session'),
        Index('idx_previous_repetition_level', 'previous_level_id'),
        Index('idx_new_repetition_level', 'new_level_id'),
    )

    def __repr__(self) -> str:
        return f"student {self.student_id} repetition in {self.academic_session} was actioned by {self.status_updated_staff}"



class Promotion(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """Represents a student's promotion to a new class"""
    __tablename__ = 'promotions'
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='CASCADE',name='fk_repetitions_students_student_id')
        )
    academic_session: Mapped[str] = mapped_column(String(9))
    previous_level_id: Mapped[UUID] = mapped_column(ForeignKey('academic_levels.id',
            ondelete='RESTRICT',name='fk_promotions_academic_levels_previous_level')
        )
    new_level_id: Mapped[UUID] = mapped_column(ForeignKey('academic_levels.id',
            ondelete='RESTRICT',name='fk_promotions_academic_levels_new_level')
        )
    status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus, name='approvalstatus'), default=ApprovalStatus.PENDING)
    status_updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id',
            ondelete='RESTRICT',name='fk_repetitions_staff_status_updated_by'),nullable=True
        )
    status_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    promoted_student: Mapped['Student'] = relationship(back_populates='promotions',
                        foreign_keys='[Promotion.student_id]', passive_deletes=True)
    previous_level: Mapped['AcademicLevel'] = relationship(foreign_keys='[Promotion.previous_level_id]')
    new_level:Mapped['AcademicLevel'] =  relationship( foreign_keys='[Promotion.new_level_id]')
    status_updated_staff:Mapped['Staff'] =  relationship(foreign_keys='[Promotion.status_updated_by]')

    __table_args__ = (
        Index('idx_promotion_status', 'student_id', 'status'),
        Index('idx_promotion_academic_session', 'student_id', 'academic_session'),
        Index('idx_previous_promotion_level', 'previous_level_id'),
        Index('idx_new_promotion_level', 'new_level_id'),
    )


class Graduation(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """Represents a student's graduation from the institution"""
    __tablename__ = 'graduations'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
                    ondelete='CASCADE', name='fk_graduations_students_student_id')
        )
    academic_session: Mapped[str] = mapped_column(String(9))
    status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus, name='approvalstatus'),
            default=ApprovalStatus.PENDING)
    status_updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id',
            ondelete='RESTRICT', name='fk_graduations_staff_status_updated_by'),
                    nullable=True)
    status_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    graduated_student: Mapped['Student'] = relationship(back_populates='graduation',
                foreign_keys='[Graduation.student_id]', passive_deletes=True)
    status_updated_staff: Mapped['Staff'] = relationship(foreign_keys='[Graduation.status_updated_by]')

    __table_args__ = (
        Index('idx_graduation_status', 'student_id', 'status'),
    )


from V2.app.core.identity.models.student import Student
from V2.app.core.identity.models.staff import Staff
from V2.app.core.academic_structure.models import AcademicLevel, Classes