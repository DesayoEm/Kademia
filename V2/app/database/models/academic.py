from app.database.models.common_imports import *
from app.database.models.data_enums import (
        ClassLevel, Term, ApprovalStatus, SubjectDepartmentType,
        GradeType, DepartmentType)

from app.database.models.mixins import AuditMixins, SoftDeleteMixins, TimeStampMixins
import uuid

class Subjects(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'subjects'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    name: Mapped[str] = mapped_column(String(30))
    class_level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel))
    department_type: Mapped[SubjectDepartmentType] = mapped_column(Enum(SubjectDepartmentType))
    is_compulsory: Mapped[bool] = mapped_column(default = True)



class Grades(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'grades'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    student_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    subject_id: Mapped[UUID] =mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    department_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    academic_year: Mapped[int] = mapped_column(Integer)
    term: Mapped[Term] = mapped_column(Enum(Term))
    type: Mapped[GradeType] = mapped_column(Enum(GradeType))
    marks: Mapped[int] = mapped_column(Integer)
    file_url: Mapped[str] = mapped_column(String(300), nullable = True)
    graded_by: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)

    __table_args__ = (
        Index('idx_subject_id', 'subject_id'),
        Index('idx_marks', 'marks'),
        Index('idx_graded_by', 'graded_by'),
        Index('idx_grade_academic_year', 'academic_year')
    )


class TotalGrades(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'total_grades'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    student_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    subject_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    academic_year: Mapped[int] = mapped_column(Integer)
    term: Mapped[Term] = mapped_column(Enum(Term))
    total_marks: Mapped[float] = mapped_column(Float)
    rank: Mapped[Optional[int]] = mapped_column(Integer, nullable = True)



    __table_args__ = (
        UniqueConstraint('student_id', 'subject_id', 'academic_year', 'term'),
        Index('idx_total_grade_subject_id', 'id'),
        Index('idx_total_marks', 'total_marks'),
        Index('idx_total_grade_academic_year', 'academic_year')
    )



class StudentSubjects(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'student_subjects'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    student_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    subject_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    academic_year: Mapped[int] = mapped_column(Integer)
    term: Mapped[Term] = mapped_column(Enum(Term))
    is_active: Mapped[bool] = mapped_column(Boolean, default = True)
    title: Mapped[str] = mapped_column(String(50))

    #Relationships


class EducatorSubjects(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'educator_subjects'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    educator_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    subject_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    term: Mapped[Term] = mapped_column(Enum(Term))
    academic_year: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default = False)


class Repetitions(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'repetitions'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    student_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    academic_year: Mapped[int] = mapped_column(Integer)
    from_class_level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel))
    to_class_level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel))
    from_class_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    to_class_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    reason: Mapped[str] = mapped_column(String(500))
    status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING)
    status_updated_by: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    status_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    __table_args__ = (
        Index('idx_repetition_status', 'status'),
        Index('idx_student_status', 'student_id', 'status'),
        Index('idx_student_academic_year', 'student_id', 'academic_year'),
        Index('idx_from_class', 'from_class_id'),
        Index('idx_to_class', 'to_class_id'),
    )

class StudentTransfers(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'student_transfers'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    student_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    academic_year: Mapped[int] = mapped_column(Integer)

    from_class_level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel))
    to_class_level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel))
    from_department: Mapped[DepartmentType] = mapped_column(Enum(DepartmentType))
    to_department: Mapped[DepartmentType] = mapped_column(Enum(DepartmentType))
    reason: Mapped[str] = mapped_column(String(500))
    status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING)
    status_updated_by: Mapped[UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    status_updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    rejection_reason: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


    __table_args__ = (
        Index('idx_transfer_status', 'status'),
        Index('idx_student_transfer_status', 'student_id', 'status'),
        Index('idx_student-transfer_academic_year', 'student_id', 'academic_year'),
        Index('idx_from_department', 'from_department'),
        Index('idx_to_department', 'to_department'),
    )

