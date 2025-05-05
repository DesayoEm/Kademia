from V2.app.core.shared.models.common_imports import *
from V2.app.core.shared.models.mixins import AuditMixins, TimeStampMixins, ArchiveMixins
from V2.app.core.shared.models.enums import Term, GradeType


class Grade(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """Represents a student's grade"""
    __tablename__ = 'grades'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
                                                        ondelete='CASCADE', name='fk_grades_students_student_id')
                                             )
    student_subject_id: Mapped[UUID] = mapped_column(
        ForeignKey('student_subjects.id', ondelete='RESTRICT',
                   name='fk_grades_student_subjects_id'))
    academic_session: Mapped[str] = mapped_column(String(9))
    term: Mapped[Term] = mapped_column(Enum(Term, name='term'))
    type: Mapped[GradeType] = mapped_column(Enum(GradeType, name='gradetype'))
    max_score: Mapped[int] = mapped_column(Integer)
    score: Mapped[float] = mapped_column(Float)
    weight: Mapped[float] = mapped_column(Float)
    file_url: Mapped[str] = mapped_column(String(225), nullable=True)
    feedback: Mapped[str] = mapped_column(String(500), nullable=True)
    graded_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id',
                                                       ondelete='RESTRICT', name='fk_grades_educator_graded_by'))
    graded_on: Mapped[pydate] = mapped_column(Date)

    # Relationships
    student: Mapped['Student'] = relationship(back_populates='grades', foreign_keys='[Grade.student_id]',
                                              passive_deletes=True)
    grader: Mapped['Educator'] = relationship(foreign_keys="[Grade.graded_by]")
    student_subject: Mapped['StudentSubject'] = relationship(back_populates='grades',
                                                             foreign_keys='[Grade.student_subject_id]')

    __table_args__ = (
        Index('idx_student_subject_id', 'student_subject_id'),
        Index('idx_score', 'score'),
        Index('idx_graded_by', 'graded_by'),
        Index('idx_grade_academic_session', 'academic_session'),
        Index('idx_student_grades', 'student_id', 'academic_session', 'term'),
        Index('idx_student_subject_term_score', 'student_subject_id', 'term', 'score')
    )


class TotalGrade(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """Represents total grades for a student in a subject"""
    __tablename__ = 'total_grades'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
    ondelete='CASCADE', name='fk_total_grades_students_student_id'))

    student_subject_id: Mapped[UUID] = mapped_column(
        ForeignKey('student_subjects.id', ondelete='RESTRICT',
                   name='fk_total_grades_student_subjects_id'))
    academic_session: Mapped[str] = mapped_column(String(9))
    term: Mapped[Term] = mapped_column(Enum(Term, name='term'))
    total_score: Mapped[int] = mapped_column(Integer)
    rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationships
    student: Mapped['Student'] = relationship(back_populates='total_grades',
        foreign_keys='[TotalGrade.student_id]',passive_deletes=True)
    student_subject: Mapped['StudentSubject'] = relationship(back_populates='total_grades',
        foreign_keys='[TotalGrade.student_subject_id]')

    __table_args__ = (
        UniqueConstraint('student_id', 'student_subject_id', 'academic_session', 'term'),
        Index('idx_total_grade_student_subject', 'student_id', 'student_subject_id'),
        Index('idx_total_grade_term', 'term'),
        Index('idx_total_grade_score', 'total_score')
    )

from V2.app.core.identity.models.student import Student
from V2.app.core.identity.models.staff import Educator
from V2.app.core.curriculum.models.curriculum import StudentSubject
