from V2.app.core.shared.models.common_imports import *
from V2.app.core.shared.models.mixins import AuditMixins, TimeStampMixins, ArchiveMixins
from V2.app.core.shared.models.enums import Term, GradeType, ApprovalStatus


class Grade(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
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
    subject: Mapped['Subject'] = relationship(back_populates='grades', foreign_keys='[Grade.subject_id]')
    student: Mapped['Student'] = relationship(back_populates='grades', foreign_keys='[Grade.student_id]',
             passive_deletes=True)
    grader: Mapped['Educator'] = relationship(foreign_keys="[Grade.graded_by]")

    __table_args__ = (
        Index('idx_subject_id', 'subject_id'),
        Index('idx_score', 'score'),
        Index('idx_graded_by', 'graded_by'),
        Index('idx_grade_academic_year', 'academic_year'),
        Index('idx_student_grades', 'student_id', 'academic_year', 'term'),
        Index('idx_student_subject_term_score', 'student_id', 'subject_id', 'term', 'score')
    )


class TotalGrade(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
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
    student: Mapped['Student'] = relationship(back_populates='total_grades', foreign_keys='[TotalGrade.student_id]',
             passive_deletes=True)
    subject: Mapped['Subject'] = relationship(back_populates='total_grades', foreign_keys='[TotalGrade.subject_id]')

    __table_args__ = (
        UniqueConstraint('student_id', 'subject_id', 'academic_year', 'term'),
        Index('idx_total_grade_subject_student', 'student_id', 'subject_id'),
        Index('idx_total_score', 'total_score'),
        Index('idx_total_grade_academic_year', 'academic_year')
    )


class Repetition(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
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
    repeating_student: Mapped['Student'] = relationship(back_populates='classes_repeated',
                        foreign_keys='[Repetition.student_id]', passive_deletes=True)
    previous_level: Mapped['AcademicLevel'] = relationship(foreign_keys='[Repetition.previous_level_id]')
    new_level:Mapped['AcademicLevel'] =  relationship( foreign_keys='[Repetition.new_level_id]')
    previous_class: Mapped['Classes'] = relationship(foreign_keys='[Repetition.previous_class_id]')
    new_class:Mapped['Classes'] =  relationship( foreign_keys='[Repetition.new_class_id]')
    status_updated_staff:Mapped['Staff'] =  relationship(foreign_keys='[Repetition.status_updated_by]')

    __table_args__ = (
        Index('idx_student_repetition_status', 'student_id', 'status'),
        Index('idx_student_academic_year', 'student_id', 'academic_year'),
        Index('idx_previous_level', 'previous_level_id'),
        Index('idx_new_level', 'new_level_id'),
    )

    def __repr__(self) -> str:
        return f"student {self.student_id} repetition in {self.academic_year} was actioned by {self.status_updated_staff}"

from V2.app.core.identity.models.student import Student
from V2.app.core.identity.models.staff import Educator, Staff
from V2.app.core.curriculum.models.curriculum import Subject
from V2.app.core.academic_structure.models.academic_structure import AcademicLevel, Classes