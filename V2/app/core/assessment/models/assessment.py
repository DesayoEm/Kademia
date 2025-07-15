from V2.app.core.shared.models.common_imports import *
from V2.app.core.shared.models.mixins import AuditMixins, TimeStampMixins, ArchiveMixins
from V2.app.core.shared.models.enums import Term, GradeType


class Grade(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """Represents a student's grade"""
    __tablename__ = 'grades'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='RESTRICT', name='fk_grades_students_student_id')
    ) #redundant column but faster for queries idc

    student_subject_id: Mapped[UUID] = mapped_column(
        ForeignKey('student_subjects.id', ondelete='RESTRICT',
                   name='fk_grades_student_subjects_id'))
    type: Mapped[GradeType] = mapped_column(Enum(GradeType, name='gradetype'))
    max_score: Mapped[int] = mapped_column(Integer)
    score: Mapped[float] = mapped_column(Float)
    weight: Mapped[int] = mapped_column(Float)
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
        Index('idx_student_score', 'student_id', 'student_subject_id', 'score'),
    )


class TotalGrade(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """Represents total grades for a student in a subject"""
    __tablename__ = 'total_grades'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
                ondelete='RESTRICT', name='fk_grades_students_student_id')
        )  # redundant column but faster for queries idc

    student_subject_id: Mapped[UUID] = mapped_column(
        ForeignKey('student_subjects.id', ondelete='RESTRICT',
                   name='fk_total_grades_student_subjects_id'), unique = True)
    total_score: Mapped[int] = mapped_column(Integer)

    # Relationships
    student_subject: Mapped['StudentSubject'] = relationship(back_populates='total_grade',
        foreign_keys='[TotalGrade.student_subject_id]')
    student: Mapped['Student'] = relationship(
        back_populates='total_grades', foreign_keys='[TotalGrade.student_id]')

    __table_args__ = (
        Index('idx_total_grade_score', 'total_score'),
    )


from V2.app.core.identity.models.student import Student
from V2.app.core.identity.models.staff import Educator
from V2.app.core.curriculum.models.curriculum import StudentSubject
