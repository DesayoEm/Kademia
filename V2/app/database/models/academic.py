from .common_imports import *
from .data_enums import (ClassLevel, Term, ApprovalStatus, SubjectGroup, GradeType, DepartmentName)
from .mixins import AuditMixins, ArchiveMixins, TimeStampMixins

class Subjects(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents an educational subject with attributes like name, class level,
    department, and compulsory status. Includes relationships to grades, students,
    and educators.

    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'subjects'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    name: Mapped[str] = mapped_column(String(30))
    class_level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel, name = 'classlevel'))
    group: Mapped[SubjectGroup] = mapped_column(Enum(SubjectGroup, name = 'subjectgroup'))
    is_elective: Mapped[bool] = mapped_column(default = True)
    syllabus_url: Mapped[str] = mapped_column(String(225), nullable = True)
    educator_id: Mapped[UUID] = mapped_column(ForeignKey('educators.id', ondelete='RESTRICT'))


    #Relationships
    students: Mapped[List['StudentSubjects']] = relationship(back_populates='subject')
    educator: Mapped['Educator'] =  relationship(back_populates='subjects', foreign_keys='[Subjects.educator_id]')
    grades: Mapped[List['Grades'] ]= relationship(back_populates='subject')
    total_grades: Mapped[List['TotalGrades']] = relationship(back_populates='subject')



class StudentSubjects(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
   Association table representing a student's enrollment in a subject for a specific academic year and term."""
    __tablename__ = 'student_subjects'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id', ondelete='CASCADE'))
    subject_id: Mapped[UUID] = mapped_column(ForeignKey('subjects.id', ondelete='RESTRICT'))
    academic_year: Mapped[str] = mapped_column(String(9))
    term: Mapped[Term] = mapped_column(Enum(Term, name='term'))
    is_active: Mapped[bool] = mapped_column(Boolean, default = True)

    __table_args__ = (
        UniqueConstraint('student_id', 'subject_id', 'academic_year', 'term'),)


    #Relationships
    subject: Mapped['Subjects'] = relationship(back_populates='students', foreign_keys='[StudentSubjects.subject_id]')
    student: Mapped['Students']= relationship(back_populates='subjects_taken', foreign_keys='[StudentSubjects.student_id]')


class Grades(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents student grades, linking students, subjects, departments, and educators.
    Includes attributes for academic year, term, grade type, and marks, with optional file URL.

    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'grades'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id', ondelete='CASCADE'))
    subject_id: Mapped[UUID] = mapped_column(ForeignKey('subjects.id', ondelete='RESTRICT'))
    academic_year: Mapped[str] = mapped_column(String(9))
    term: Mapped[Term] = mapped_column(Enum(Term, name='term'))
    type: Mapped[GradeType] = mapped_column(Enum(GradeType, name='gradetype'))
    marks: Mapped[int] = mapped_column(Integer)
    file_url: Mapped[str] = mapped_column(String(300), nullable = True)
    feedback: Mapped[str] = mapped_column(String(300), nullable = True)
    graded_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id', ondelete='RESTRICT'))

    #Relationships
    subject: Mapped['Subjects'] = relationship(back_populates='grades', foreign_keys='[Grades.subject_id]')
    student: Mapped['Students'] = relationship(back_populates='grades', foreign_keys='[Grades.student_id]')
    grader: Mapped['Educator'] = relationship(foreign_keys="[Grades.graded_by]")
    department: Mapped['Departments'] = relationship(foreign_keys="[Grades.department_id]")


    __table_args__ = (
        Index('idx_subject_id', 'subject_id'),
        Index('idx_marks', 'marks'),
        Index('idx_graded_by', 'graded_by'),
        Index('idx_grade_academic_year', 'academic_year')
    )


class TotalGrades(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
   Represents total grades for a student in a subject, including total marks, rank,
   academic year, and term. Links students and subjects with unique constraints on
   student, subject, academic year, and term.

   Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
   """
    __tablename__ = 'total_grades'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id', ondelete='CASCADE'))
    subject_id: Mapped[UUID] = mapped_column(ForeignKey('subjects.id', ondelete='RESTRICT'))
    academic_year: Mapped[str] = mapped_column(String(9))
    term: Mapped[Term] = mapped_column(Enum(Term, name='term'))
    total_marks: Mapped[float] = mapped_column(Float)
    rank: Mapped[Optional[int]] = mapped_column(Integer, nullable = True)

    #Relationships
    student: Mapped['Students'] = relationship(back_populates='total_grades', foreign_keys='[TotalGrades.student_id]')
    subject: Mapped['Subjects'] = relationship(back_populates='total_grades', foreign_keys='[TotalGrades.subject_id]')


    __table_args__ = (
        UniqueConstraint('student_id', 'subject_id', 'academic_year', 'term'),
        Index('idx_total_grade_subject_id', 'subject_id'),
        Index('idx_total_marks', 'total_marks'),
        Index('idx_total_grade_academic_year', 'academic_year')
    )


class Repetitions(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
     Represents a student's repetition of a class, including details like class level change,
     reason for repetition, approval status, and class assignments.

     Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
     """
    __tablename__ = 'repetitions'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id', ondelete='CASCADE'))
    academic_year: Mapped[int] = mapped_column(Integer)
    from_class_level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel, name = 'classlevel'))
    to_class_level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel, name = 'classlevel'))
    from_class_id: Mapped[UUID] = mapped_column(ForeignKey ('classes.id',ondelete='RESTRICT'))
    to_class_id: Mapped[UUID] = mapped_column(ForeignKey ('classes.id', ondelete='RESTRICT'))
    reason: Mapped[str] = mapped_column(String(500))
    status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus, name = 'approvalstatus'), default=ApprovalStatus.PENDING)
    status_updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id', ondelete='RESTRICT'), nullable=True)
    status_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    #Relationships
    repeater:Mapped['Students'] = relationship(back_populates='classes_repeated', foreign_keys='[Repetitions.student_id]')
    from_class:Mapped['Classes'] = relationship(foreign_keys='[Repetitions.from_class_id]')
    to_class:Mapped['Classes'] =  relationship( foreign_keys='[Repetitions.to_class_id]')
    status_updated_staff:Mapped['Staff'] =  relationship(foreign_keys='[Repetitions.status_updated_by]')

    __table_args__ = (
        Index('idx_repetition_status', 'status'),
        Index('idx_student_status', 'student_id', 'status'),
        Index('idx_student_academic_year', 'student_id', 'academic_year'),
        Index('idx_from_class', 'from_class_id'),
        Index('idx_to_class', 'to_class_id'),
    )

    def __repr__(self) -> str:
        return f"student {self.student_id} repetition in {self.academic_year} was actioned by {self.status_updated_staff}"


class StudentTransfers(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
   Represents a student's transfer between departments or class levels, including the reason,
   approval status, and status updates.

   Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
   """
    __tablename__ = 'student_transfers'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id', ondelete='CASCADE'))
    academic_year: Mapped[int] = mapped_column(Integer)
    from_class_level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel, name='classlevel'))
    to_class_level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel, name='classlevel'))
    from_class_id: Mapped[UUID] = mapped_column(ForeignKey ('classes.id',ondelete='RESTRICT'))
    to_class_id: Mapped[UUID] = mapped_column(ForeignKey ('classes.id', ondelete='RESTRICT'))
    from_department_id: Mapped[UUID] = mapped_column(ForeignKey('departments.id', ondelete='RESTRICT'))
    to_department_id: Mapped[UUID] = mapped_column(ForeignKey('departments.id', ondelete='RESTRICT'))
    reason: Mapped[str] = mapped_column(String(500))
    status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus, name='approvalstatus'), default=ApprovalStatus.PENDING)
    status_updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id', ondelete='RESTRICT'), nullable=True)
    status_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    #Relationships
    transferred_student: Mapped['Students'] = relationship(back_populates='transfers',foreign_keys='[StudentTransfers.student_id]')
    from_dept: Mapped['Departments'] = relationship(foreign_keys='[StudentTransfers.from_department_id]')
    to_dept: Mapped['Departments'] = relationship('Departments', foreign_keys='[StudentTransfers.to_department_id]')
    from_class: Mapped['Classes'] = relationship(foreign_keys='[StudentTransfers.from_class_id]')
    to_class: Mapped['Classes'] = relationship('Departments', foreign_keys='[StudentTransfers.to_class_id]')
    status_updater: Mapped ['Staff'] = relationship(foreign_keys='[StudentTransfers.status_updated_by]')

    __table_args__ = (
        Index('idx_transfer_status', 'status'),
        Index('idx_student_transfer_status', 'student_id', 'status'),
        Index('idx_student-transfer_academic_year', 'student_id', 'academic_year'),
        Index('idx_from_department_id', 'from_department_id'),
        Index('idx_to_department_id', 'to_department_id'),
    )

    def __repr__(self) -> str:
        return f"student {self.student_id} transfer from {self.from_department_id} to {self.to_department_id} in {self.academic_year}\
        was actioned by {self.status_updater}"


class EducatorQualifications(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents an educator's assignment to a subject for a specific academic year and term.
    Includes attributes like active status and term.

    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'educator_qualifications'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    educator_id: Mapped[UUID] = mapped_column(ForeignKey('educators.id', ondelete='CASCADE'))

    #Relationships
    educator = relationship('Educator', back_populates='qualifications', foreign_keys="[EducatorQualifications.educator_id]")

