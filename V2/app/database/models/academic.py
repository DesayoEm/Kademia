from .common_imports import *
from .data_enums import (Term, ApprovalStatus, GradeType)
from .mixins import AuditMixins, ArchiveMixins, TimeStampMixins


class Subjects(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents an educational subject with attributes like name, class level,
    department, and compulsory status. Includes relationships to grades, students,
    and educators.

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
    students: Mapped[List['StudentSubjects']] = relationship(back_populates='subject')
    educators: Mapped[List['SubjectEducators']] = relationship(back_populates='subject')
    academic_levels: Mapped[List['AcademicLevelSubjects']] = relationship(back_populates='subject')
    grades: Mapped[List['Grades']] = relationship(back_populates='subject')
    total_grades: Mapped[List['TotalGrades']] = relationship(back_populates='subject')

    __table_args__ = (
        Index('idx_subject_name', 'name'),
        Index('idx_subject_department', 'department_id'),
    )


class AcademicLevelSubjects(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
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
    subject: Mapped['Subjects'] = relationship(back_populates='academic_levels', foreign_keys='[AcademicLevelSubjects.subject_id]')
    level: Mapped['AcademicLevel'] = relationship(back_populates='subjects', foreign_keys='[AcademicLevelSubjects.level_id]')

    __table_args__ = (
        UniqueConstraint('level_id', 'subject_id', 'academic_year', 'educator_id'),
        Index('idx_level_subject', 'level_id', 'subject_id'),
        Index('idx_level_subject_educator', 'level_id', 'subject_id', 'educator_id'),
    )


class StudentSubjects(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
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
    subject: Mapped['Subjects'] = relationship(back_populates='students', foreign_keys='[StudentSubjects.subject_id]')
    student: Mapped['Students'] = relationship(back_populates='subjects_taken', foreign_keys='[StudentSubjects.student_id]')

    __table_args__ = (
        UniqueConstraint('student_id', 'subject_id', 'academic_year', 'term'),
        Index('idx_student_subject_term', 'student_id', 'subject_id', 'term', 'academic_year')
    )


class SubjectEducators(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
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
    subject: Mapped['Subjects'] = relationship(back_populates='educators', foreign_keys='[SubjectEducators.subject_id]')
    teacher: Mapped['Educator'] = relationship(back_populates='subject_assignments', foreign_keys='[SubjectEducators.educator_id]')

    __table_args__ = (
        UniqueConstraint('educator_id', 'subject_id', 'academic_year', 'term', 'level_id'),
        Index('idx_subject_level_educator', 'educator_id', 'level_id', 'subject_id')
    )


class Grades(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents student grades, linking students, subjects, departments, and educators.
    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'grades'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='CASCADE',name='fk_grades_students_student_id')
        )
    subject_id: Mapped[UUID] = mapped_column(ForeignKey('subjects.id',
            ondelete='RESTRICT',name='fk_grades_subjects_subject_id')
        )
    academic_year: Mapped[str] = mapped_column(String(9))
    term: Mapped[Term] = mapped_column(Enum(Term, name='term'))
    type: Mapped[GradeType] = mapped_column(Enum(GradeType, name='gradetype'))
    score: Mapped[int] = mapped_column(Integer)
    file_url: Mapped[str] = mapped_column(String(225), nullable=True)
    feedback: Mapped[str] = mapped_column(String(500), nullable=True)
    graded_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id',
            ondelete='RESTRICT',name='fk_grades_staff_graded_by')
        )

    # Relationships
    subject: Mapped['Subjects'] = relationship(back_populates='grades', foreign_keys='[Grades.subject_id]')
    student: Mapped['Students'] = relationship(back_populates='grades', foreign_keys='[Grades.student_id]')
    grader: Mapped['Educator'] = relationship(foreign_keys="[Grades.graded_by]")

    __table_args__ = (
        Index('idx_subject_id', 'subject_id'),
        Index('idx_score', 'score'),
        Index('idx_graded_by', 'graded_by'),
        Index('idx_grade_academic_year', 'academic_year'),
        Index('idx_student_grades', 'student_id', 'academic_year', 'term'),
        Index('idx_student_subject_term_score', 'student_id', 'subject_id', 'term', 'score')
    )


class TotalGrades(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents total grades for a student in a subject, including total score, rank,
    academic year, and term. Links students and subjects with unique constraints on
    student, subject, academic year, and term.

    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'total_grades'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='CASCADE',name='fk_total_grades_students_student_id')
        )
    subject_id: Mapped[UUID] = mapped_column(ForeignKey('subjects.id',
            ondelete='RESTRICT',name='fk_total_grades_subjects_subject_id')
        )
    academic_year: Mapped[str] = mapped_column(String(9))
    term: Mapped[Term] = mapped_column(Enum(Term, name='term'))
    total_score: Mapped[int] = mapped_column(Integer
                                             )
    rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationships
    student: Mapped['Students'] = relationship(back_populates='total_grades', foreign_keys='[TotalGrades.student_id]')
    subject: Mapped['Subjects'] = relationship(back_populates='total_grades', foreign_keys='[TotalGrades.subject_id]')

    __table_args__ = (
        UniqueConstraint('student_id', 'subject_id', 'academic_year', 'term'),
        Index('idx_total_grade_subject_student', 'student_id', 'subject_id'),
        Index('idx_total_score', 'total_score'),
        Index('idx_total_grade_academic_year', 'academic_year')
    )


class StudentRepetitions(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents a student's repetition of a class, including details like class level change,
    reason for repetition, approval status, and class assignments.

    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'student_repetitions'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='CASCADE',name='fk_student_repetitions_students_student_id')
        )
    academic_year: Mapped[int] = mapped_column(Integer)
    previous_level_id: Mapped[UUID] = mapped_column(ForeignKey('academic_levels.id',
            ondelete='RESTRICT',name='fk_student_repetitions_academic_levels_previous_level')
        )
    new_level_id: Mapped[UUID] = mapped_column(ForeignKey('academic_levels.id',
            ondelete='RESTRICT',name='fk_student_repetitions_academic_levels_new_level')
        )
    previous_class_id: Mapped[UUID] = mapped_column(ForeignKey('classes.id',
            ondelete='RESTRICT',name='fk_student_repetitions_classes_previous_class')
        )
    new_class_id: Mapped[UUID] = mapped_column(ForeignKey('classes.id',
            ondelete='RESTRICT', name='fk_student_repetitions_classes_new_class')
        )
    reason: Mapped[str] = mapped_column(String(500))
    status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus, name='approvalstatus'), default=ApprovalStatus.PENDING)
    status_updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id',
            ondelete='RESTRICT',name='fk_student_repetitions_staff_status_updated_by'),nullable=True
        )
    status_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    repeating_student: Mapped['Students'] = relationship(back_populates='classes_repeated', foreign_keys='[StudentRepetitions.student_id]')
    previous_level: Mapped['AcademicLevel'] = relationship(foreign_keys='[StudentRepetitions.previous_level_id]')
    new_level:Mapped['AcademicLevel'] =  relationship( foreign_keys='[StudentRepetitions.new_level_id]')
    previous_class: Mapped['Classes'] = relationship(foreign_keys='[StudentRepetitions.previous_class_id]')
    new_class:Mapped['Classes'] =  relationship( foreign_keys='[StudentRepetitions.new_class_id]')
    status_updated_staff:Mapped['Staff'] =  relationship(foreign_keys='[StudentRepetitions.status_updated_by]')

    __table_args__ = (
        Index('idx_student_repetition_status', 'student_id', 'status'),
        Index('idx_student_academic_year', 'student_id', 'academic_year'),
        Index('idx_previous_level', 'previous_level_id'),
        Index('idx_new_level', 'new_level_id'),
    )

    def __repr__(self) -> str:
        return f"student {self.student_id} repetition in {self.academic_year} was actioned by {self.status_updated_staff}"


