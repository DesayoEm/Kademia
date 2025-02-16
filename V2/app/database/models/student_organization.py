from .common_imports import *
from .mixins import AuditMixins, ArchiveMixins, TimeStampMixins
from .data_enums import ClassCode


class AcademicLevel(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents an academic level (e.g., JSS1, SSS1) with its curriculum requirements
    """
    __tablename__ = 'academic_levels'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str] = mapped_column(String(500))
    order: Mapped[int] = mapped_column(Integer)

    # Relationships
    classes: Mapped[List['Classes']] = relationship(back_populates='academic_level')
    subjects: Mapped[List['AcademicLevelSubjects']] = relationship(back_populates='level')
    students: Mapped[List['Students']] = relationship(back_populates='level')

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
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey('educators.id',
            ondelete='RESTRICT', name='fk_classes_educators_mentor_id'), nullable = True
        )
    student_rep: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='SET NULL', name='fk_classes_students_student_rep'), nullable=True
        )
    assistant_rep: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='SET NULL', name='fk_classes_students_assistant_rep'), nullable=True
        )

    # Relationships
    students: Mapped[List['Students']] = relationship(
        back_populates='class_', foreign_keys='[Students.class_id]',
        primaryjoin='Classes.id == Students.class_id'
    )
    academic_level: Mapped['AcademicLevel'] = relationship(
        back_populates='classes', foreign_keys='[Classes.level_id]'
    )
    mentor: Mapped['Educator'] = relationship(
        back_populates='mentored_class', foreign_keys='[Classes.mentor_id]'
    )
    class_rep: Mapped['Students'] = relationship(foreign_keys='[Classes.student_rep]')
    assist_rep: Mapped['Students'] = relationship(foreign_keys='[Classes.assistant_rep]')

    __table_args__ = (
        UniqueConstraint('level_id', 'code', name='uq_class_level_code'),
        Index('idx_class_level_code', 'level_id', 'code'),
        Index('idx_class_mentor', 'mentor_id'),
        Index('idx_class_reps', 'student_rep', 'assistant_rep')
    )

    def __repr__(self) -> str:
        return f"Class(level={self.level_id}, code={self.code}, mentor={self.mentor_id})"


class StudentDepartments(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents a department within an educational institution, including its name, code,
    description, and associated mentor. Links to students and educator mentor relationships.

    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'student_departments'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str] = mapped_column(String(500))
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey('educators.id',
            ondelete='RESTRICT', name='fk_student_departments_educators_mentor_id'), nullable=True
        )
    student_rep: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='SET NULL', name='fk_student_departments_students_student_rep'), nullable=True
        )
    assistant_rep: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='SET NULL', name='fk_student_departments_students_assistant_rep'), nullable=True
        )

    # Relationships
    students: Mapped[List['Students']] = relationship(back_populates='department')
    mentor: Mapped['Educator'] = relationship(
        back_populates='mentored_department', foreign_keys='[StudentDepartments.mentor_id]'
    )

    __table_args__ = (
        Index('idx_department_mentor', 'mentor_id'),
        Index('idx_department_name', 'name'),
        Index('idx_department_reps', 'student_rep', 'assistant_rep')
    )
