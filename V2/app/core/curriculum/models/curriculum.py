from V2.app.core.shared.models.common_imports import *
from V2.app.core.shared.models.mixins import AuditMixins, TimeStampMixins, ArchiveMixins
from V2.app.core.shared.models.enums import Term

class Subject(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents an educational subject
    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'subjects'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(30))
    department_id: Mapped[UUID] = mapped_column(ForeignKey('student_departments.id',
            ondelete='RESTRICT',name='fk_subjects_student_departments_department_id')
        )
    is_elective: Mapped[bool] = mapped_column(default=True)
    syllabus_url: Mapped[str] = mapped_column(String(225), nullable=True)

    # Relationships
    students: Mapped[List['StudentSubject']] = relationship(back_populates='subject')
    educators: Mapped[List['SubjectEducator']] = relationship(back_populates='subject')
    academic_levels: Mapped[List['AcademicLevelSubject']] = relationship(back_populates='subject')
    grades: Mapped[List['Grade']] = relationship(back_populates='subject')
    total_grades: Mapped[List['TotalGrade']] = relationship(back_populates='subject')

    __table_args__ = (
        Index('idx_subject_name', 'name'),
        Index('idx_subject_department', 'department_id'),
    )


class AcademicLevelSubject(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """Associates subjects with academic levels, defining the standard curriculum"""
    __tablename__ = 'academic_level_subjects'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    level_id: Mapped[UUID] = mapped_column(ForeignKey('academic_levels.id',
                ondelete='RESTRICT',name='fk_academic_level_subjects_academic_levels_level_id')
        )
    subject_id: Mapped[UUID] = mapped_column(ForeignKey('subjects.id',
            ondelete='RESTRICT',name='fk_academic_level_subjects_subjects_subject_id')
        )
    educator_id: Mapped[UUID] = mapped_column(ForeignKey('educators.id',
            ondelete='RESTRICT',name='fk_academic_level_subjects_educators_educator_id')
        )
    is_elective: Mapped[bool] = mapped_column(Boolean, default=False)
    academic_year: Mapped[str] = mapped_column(String(9))
    curriculum_url: Mapped[str] = mapped_column(String(225))

    # Relationships
    subject: Mapped['Subject'] = relationship(back_populates='academic_levels', foreign_keys='[AcademicLevelSubject.subject_id]')
    level: Mapped['AcademicLevel'] = relationship(back_populates='subjects', foreign_keys='[AcademicLevelSubject.level_id]')

    __table_args__ = (
        UniqueConstraint('level_id', 'subject_id', 'academic_year', 'educator_id'),
        Index('idx_level_subject', 'level_id', 'subject_id'),
        Index('idx_level_subject_educator', 'level_id', 'subject_id', 'educator_id'),
    )


class StudentSubject(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """Association table representing a student's enrollment in a subject for a specific academic year and term."""
    __tablename__ = 'student_subjects'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(
        ForeignKey( 'students.id',ondelete='CASCADE',
            name='fk_student_subjects_students_student_id')
        )
    subject_id: Mapped[UUID] = mapped_column(ForeignKey('subjects.id',
            ondelete='RESTRICT',name='fk_student_subjects_subjects_subject_id')
        )
    academic_year: Mapped[str] = mapped_column(String(9))
    term: Mapped[Term] = mapped_column(Enum(Term, name='term'))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    subject: Mapped['Subject'] = relationship(back_populates='students',
            foreign_keys='[StudentSubject.subject_id]')
    student: Mapped['Student'] = relationship(back_populates='subjects_taken',
            foreign_keys='[StudentSubject.student_id]', passive_deletes=True)

    __table_args__ = (
        UniqueConstraint('student_id', 'subject_id', 'academic_year', 'term'),
        Index('idx_student_subject_term', 'student_id', 'subject_id', 'term', 'academic_year')
    )


class SubjectEducator(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """Association table representing a teacher assignment to a subject for a specific academic year and term."""
    __tablename__ = 'subject_educators'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey('subjects.id',
                                                        ondelete='RESTRICT',name='fk_subject_educators_subjects_subject_id')
                                             )
    educator_id: Mapped[UUID] = mapped_column(ForeignKey('educators.id',
            ondelete='RESTRICT',name='fk_subject_educators_educators_educator_id')
        )
    level_id: Mapped[UUID] = mapped_column(ForeignKey('academic_levels.id',
            ondelete='RESTRICT',name='fk_subject_educators_academic_levels_level_id')
        )
    academic_year: Mapped[str] = mapped_column(String(9))
    term: Mapped[Term] = mapped_column(Enum(Term, name='term'))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    date_assigned: Mapped[Date] = mapped_column(Date)

    # Relationships
    subject: Mapped['Subject'] = relationship(back_populates='educators', foreign_keys='[SubjectEducator.subject_id]')
    teacher: Mapped['Educator'] = relationship(back_populates='subject_assignments', foreign_keys='[SubjectEducator.educator_id]')

    __table_args__ = (
        UniqueConstraint('educator_id', 'subject_id', 'academic_year', 'term', 'level_id'),
        Index('idx_subject_level_educator', 'educator_id', 'level_id', 'subject_id')
    )



