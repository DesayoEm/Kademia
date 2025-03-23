from .common_imports import *
from .mixins import AuditMixins, ArchiveMixins, TimeStampMixins
from .enums import ClassCode, ApprovalStatus


class AcademicLevel(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents an academic level (e.g., JSS1, SSS1) with its curriculum requirements
    """
    __tablename__ = 'academic_levels'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str] = mapped_column(String(500))
    order: Mapped[int] = mapped_column(Integer, unique=True)

    # Relationships
    classes: Mapped[List['Classes']] = relationship(back_populates='academic_level')
    subjects: Mapped[List['AcademicLevelSubject']] = relationship(back_populates='level')
    students: Mapped[List['Student']] = relationship(back_populates='level')

    __table_args__ = (
        Index('idx_academic_level_name', 'name'),
        Index('idx_academic_level_description', 'description'),
    )


class Classes(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents a physical class within the institution, including its level, code, and academic mentor.
    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'classes'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    level_id: Mapped[UUID] = mapped_column(ForeignKey('academic_levels.id',
            ondelete='RESTRICT', name='fk_classes_academic_levels_level_id')
        )
    code: Mapped[ClassCode] = mapped_column(Enum(ClassCode, name='classcode'))
    supervisor_id: Mapped[UUID] = mapped_column(ForeignKey('educators.id',
            ondelete='RESTRICT', name='fk_classes_educators_supervisor_id'), nullable = True
        )
    student_rep_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='SET NULL', name='fk_classes_students_student_rep'), nullable=True
        )
    assistant_rep_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='SET NULL', name='fk_classes_students_assistant_rep'), nullable=True
        )
    order: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)

    # Relationships
    students: Mapped[List['Student']] = relationship(
        back_populates='class_', foreign_keys='[Student.class_id]',
        primaryjoin='Classes.id == Student.class_id'
    )
    academic_level: Mapped['AcademicLevel'] = relationship(
        back_populates='classes', foreign_keys='[Classes.level_id]'
    )
    supervisor: Mapped['Educator'] = relationship(
        back_populates='supervised_class', foreign_keys='[Classes.supervisor_id]'
    )
    student_rep: Mapped['Student'] = relationship(foreign_keys='[Classes.student_rep_id]')
    assistant_rep: Mapped['Student'] = relationship(foreign_keys='[Classes.assistant_rep_id]')

    __table_args__ = (
        UniqueConstraint('level_id', 'code', name='uq_class_level_code'),
        Index('idx_class_level_code', 'level_id', 'code'),
        Index('idx_class_supervisor', 'supervisor_id'),
        Index('idx_class_reps', 'student_rep_id', 'assistant_rep_id')
    )

    def __repr__(self) -> str:
        return f"Class(level={self.level_id}, code={self.code}, mentor={self.supervisor_id})"



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
    transferred_student: Mapped['Student'] = relationship(back_populates='class_transfers', foreign_keys='[ClassTransfer.student_id]')
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


class StudentDepartment(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents a department within an educational institution, including its name, code,
    description, and associated mentor. Links to students and educator mentor relationships.

    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'student_departments'


    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    code: Mapped[str] = mapped_column(String(3), unique=True)
    description: Mapped[str] = mapped_column(String(500))
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey('educators.id',
            ondelete='RESTRICT', name='fk_student_departments_educators_mentor_id'), nullable=True
        )
    student_rep_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='RESTRICT', name='fk_student_departments_students_student_rep'), nullable=True
        )
    assistant_rep_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='RESTRICT', name='fk_student_departments_students_assistant_rep'), nullable=True
        )

    # Relationships
    students: Mapped[List['Student']] = relationship(
        'Student', back_populates='department',
        primaryjoin='StudentDepartment.id == Student.department_id'
    )
    mentor: Mapped['Educator'] = relationship(
        back_populates='mentored_department', foreign_keys='[StudentDepartment.mentor_id]'
    )

    __table_args__ = (
        Index('idx_department_mentor', 'mentor_id'),
        Index('idx_department_name', 'name'),
        Index('idx_department_code', 'code'),
        Index('idx_department_reps', 'student_rep_id', 'assistant_rep_id')
    )


class StudentDepartmentTransfer(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents a student's transfer between departments including the reason,approval status, and status updates.
    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'student_department_transfers'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
                    ondelete='CASCADE',name='fk_student_department_transfers_students_student_id')
                                             )
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
    transferred_student: Mapped['Student'] = relationship(back_populates='department_transfers', foreign_keys='[StudentDepartmentTransfer.student_id]')
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


