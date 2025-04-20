from ...shared.database.models.common_imports import *
from ...shared.database.models.mixins import AuditMixins, TimeStampMixins, ArchiveMixins
from ...shared.database.models.enums import ClassCode

class AcademicLevel(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents an academic level (e.g., JSS1, SSS1) with its curriculum requirements
    """
    __tablename__ = 'academic_levels'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True)
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
            ondelete='SET NULL', name='fk_classes_educators_supervisor_id'), nullable = True
        )
    student_rep_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='SET NULL', name='fk_classes_students_student_rep'), nullable=True
        )
    assistant_rep_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='SET NULL', name='fk_classes_students_assistant_rep'), nullable=True
        )
    order: Mapped[int] = mapped_column(Integer, nullable=False)

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
    student_rep: Mapped['Student'] = relationship(
        'Student', back_populates='represented_class',
        foreign_keys='[Classes.student_rep_id]'
    )
    assistant_rep: Mapped['Student'] = relationship(
        'Student', back_populates='assistant_represented_class',
        foreign_keys='[Classes.assistant_rep_id]'
    )

    __table_args__ = (
        UniqueConstraint('level_id', 'code', name='uq_class_level_code'),
        UniqueConstraint('level_id', 'order', name='uq_class_level_order'),
        Index('idx_class_level_code', 'level_id', 'code'),
        Index('idx_class_supervisor', 'supervisor_id'),
        Index('idx_class_reps', 'student_rep_id', 'assistant_rep_id')
    )

    def __repr__(self) -> str:
        return f"Class(level={self.level_id}, code={self.code}, mentor={self.supervisor_id})"



class StudentDepartment(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents a department within an educational institution, including its name, code,
    description, and associated mentor. Links to students and educator mentor relationships.

    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'student_departments'


    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True)
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
    student_rep: Mapped['Student'] = relationship(
        'Student', back_populates='represented_department',
        foreign_keys='[StudentDepartment.student_rep_id]'  # Fixed foreign key reference
    )
    assistant_rep: Mapped['Student'] = relationship(  # Changed type from Educator to Student
        'Student', back_populates='assistant_represented_department',
        foreign_keys='[StudentDepartment.assistant_rep_id]'  # Fixed foreign key reference
    )

