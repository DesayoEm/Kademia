from app.data.models.validators import GradeType
from base import *
from validators import ClassLevel, Term

class Subjects(Base):
    __tablename__ = 'subjects'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    name: Mapped[str] = mapped_column(String(30), nullable = False)
    class_level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel), nullable = False)
    department_id: Mapped[UUID] = mapped_column(ForeignKey('department.id'), nullable=True)
    is_compulsory: Mapped[bool] = mapped_column(default = True, Nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)

    #Relationships
    students = relationship('Students', back_populates='subjects_taken')
    creator = relationship('Staff', foreign_keys = [created_by])
    updater = relationship('Staff', foreign_keys = [updated_by])



class Grades(Base):
    __tablename__ = 'grades'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id'), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey('subjects.id'), nullable=True)
    department_id: Mapped[UUID] = mapped_column(ForeignKey('department.id'), nullable=True)
    academic_year: Mapped[int] = mapped_column(Integer, nullable=False)
    term: Mapped[Term] = mapped_column(Enum(Term), nullable = False)
    type: Mapped[GradeType] = mapped_column(Enum(GradeType), nullable = False)
    name: Mapped[str] = mapped_column(String(30), nullable = False)
    marks: Mapped[int] = mapped_column(Integer, nullable=False)
    file_url: Mapped[str] = mapped_column(String(300), nullable = True)
    graded_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)

    #Relationships
    subject = relationship('Subjects', back_populates='grades')
    student = relationship('Students', back_populates='grades')
    creator = relationship('Staff', foreign_keys = [created_by])
    updater = relationship('Staff', foreign_keys = [updated_by])

class TotalGrades(Base):
    __tablename__ = 'total_grades'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id'), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey('subjects.id'), nullable=False)
    academic_year: Mapped[int] = mapped_column(Integer, nullable=False)
    term: Mapped[Term] = mapped_column(Enum(Term), nullable=False)
    total_marks: Mapped[float] = mapped_column(Float, nullable=False)
    rank: Mapped[Optional[int]] = mapped_column(Integer)  # Class rank for this subject
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)

    # Relationships
    student = relationship('Students', back_populates='total_grades')
    subject = relationship('Subjects', back_populates='total_grades')
    creator = relationship('Staff', foreign_keys=[created_by])
    updater = relationship('Staff', foreign_keys=[updated_by])

    __table_args__ = (
        UniqueConstraint('student_id', 'subject_id', 'academic_year', 'term'),
    )


class StudentSubjects(Base):
    __tablename__ = 'student_subjects'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id'), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey('subjects.id'), nullable=True)
    academic_year: Mapped[int] = mapped_column(Integer, nullable=False)
    term: Mapped[Term] = mapped_column(Enum(Term), nullable = False)
    is_active: Mapped[bool] = mapped_column(Boolean, default = True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)

    #Relationships
    subject = relationship('Subjects', back_populates='student_subjects')
    student = relationship('Students', back_populates='subjects_taken')
    creator = relationship('Staff', foreign_keys = [created_by])
    updater = relationship('Staff', foreign_keys = [updated_by])



class EducatorSubjects(Base):
    __tablename__ = 'educator_subjects'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    educator_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)
    subject_id: Mapped[UUID] = mapped_column(ForeignKey('subjects.id'), nullable=True)
    term: Mapped[Term] = mapped_column(Enum(Term), nullable = False)
    academic_year: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)

   #Relationships
    educator = relationship('Staff', back_populates='subjects_taken')
    creator = relationship('Staff', foreign_keys = [created_by])
    updater = relationship('Staff', foreign_keys = [updated_by])



class Repetitions(Base):
    __tablename__ = 'repetitions'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id'), nullable=False)
    academic_year: Mapped[int] = mapped_column(Integer, nullable=False)
    from_class: Mapped[ClassLevel] = mapped_column(ForeignKey = 'classes.level', nullable=False)
    to_class: Mapped[ClassLevel] = mapped_column(ForeignKey = 'classes.level', nullable=False)
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    approved_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)


    #Relationships
    repeater = relationship('Students', back_populates='classes_repeated')
    creator = relationship('Staff', foreign_keys = [created_by])
    updater = relationship('Staff', foreign_keys = [updated_by])
