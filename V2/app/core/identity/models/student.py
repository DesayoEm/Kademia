from .base import UserBase

from V2.app.core.shared.models.common_imports import *
from V2.app.core.shared.models.enums import AccessLevel, StudentStatus, UserType


class Student(UserBase):
    """
    Represents a student, including personal details, enrollment information, academic status, and relationships with other entities.
    Inherits from ProfileBase.
    """
    __tablename__ = 'students'

    student_id: Mapped[str] = mapped_column(String(14), unique=True)
    guardian_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('guardians.id',
                ondelete='RESTRICT',name='fk_students_guardians_guardian_id')
            )
    user_type: Mapped[UserType] = mapped_column(Enum(UserType, name='usertype'), default=UserType.STUDENT)
    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel, name='accesslevel'), default=AccessLevel.READ)
    status: Mapped[StudentStatus] = mapped_column(Enum(StudentStatus, name='studentstatus'), default=StudentStatus.ENROLLED)
    date_of_birth: Mapped[date] = mapped_column(Date)
    image_url: Mapped[str] = mapped_column(String(200), nullable=True)
    level_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('academic_levels.id',
            ondelete='SET NULL',name='fk_students_academic_levels_level_id'), nullable = True
        )
    class_id: Mapped[UUID] = mapped_column(UUID,ForeignKey('classes.id',
            ondelete='SET NULL',name='fk_students_classes_class_id'), nullable = True
        )
    department_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),ForeignKey('student_departments.id',
            ondelete='SET NULL',name='fk_students_student_departments_department_id'),  nullable = True
        )
    is_repeating: Mapped[bool] = mapped_column(Boolean, default=False)
    session_start_year: Mapped[int] = mapped_column(Integer)
    date_left: Mapped[date] = mapped_column(Date, nullable=True)
    graduation_date: Mapped[date] = mapped_column(Date, nullable=True)

    # Relationships
    documents_owned: Mapped[List['StudentDocument']] = relationship(back_populates='owner')
    awards_earned: Mapped[List['StudentAward']] = relationship(back_populates='owner')
    guardian: Mapped['Guardian'] = relationship(back_populates='wards', foreign_keys='[Student.guardian_id]')
    class_: Mapped['Classes'] = relationship(back_populates='students',foreign_keys='[Student.class_id]',
        primaryjoin='Student.class_id == Classes.id')
    department: Mapped['StudentDepartment'] = relationship(back_populates='students', foreign_keys='[Student.department_id]')
    level: Mapped['AcademicLevel'] = relationship(back_populates='students', foreign_keys='[Student.level_id]')
    subjects_taken: Mapped[List['StudentSubject']] = relationship(back_populates='student')
    grades: Mapped[List['Grade']] = relationship(back_populates='student')
    classes_repeated: Mapped[List['Repetition']] = relationship(back_populates='repeating_student')
    promotions: Mapped[List['Promotion']] = relationship(back_populates='promoted_student')
    graduation: Mapped['Graduation'] = relationship(back_populates='graduated_student')
    department_transfers: Mapped[List['StudentDepartmentTransfer']] = relationship(back_populates='transferred_student')
    class_transfers: Mapped[List['ClassTransfer']] = relationship(back_populates='transferred_student')

    represented_department: Mapped['StudentDepartment'] = relationship(
        'StudentDepartment', back_populates='student_rep',
        primaryjoin='Student.id == StudentDepartment.student_rep_id',
        uselist=False
    )
    assistant_represented_department: Mapped['StudentDepartment'] = relationship(
        'StudentDepartment', back_populates='assistant_rep',
        primaryjoin='Student.id == StudentDepartment.assistant_rep_id',
        uselist=False
    )
    represented_class: Mapped['Classes'] = relationship(
        'Classes', back_populates='student_rep',
        primaryjoin='Student.id == Classes.student_rep_id',
        uselist=False
    )
    assistant_represented_class: Mapped['Classes'] = relationship(
        'Classes', back_populates='assistant_rep',
        primaryjoin='Student.id == Classes.assistant_rep_id',
        uselist=False
    )

    __table_args__ = (
        Index('idx_students_name', 'first_name', 'last_name'),
        Index('idx_students_id', 'student_id'),
        Index('idx_class_id', 'class_id'),
        Index('idx_level_id', 'level_id'),
        Index('idx_department_id', 'department_id'),
        Index('idx_guardian_id', 'guardian_id'),
    )

    def __repr__(self) -> str:
        return f"Student(name={self.first_name} {self.last_name}, class={self.class_})"

from V2.app.core.documents.models.documents import StudentDocument, StudentAward
from V2.app.core.identity.models.guardian import Guardian
from V2.app.core.academic_structure.models.academic_structure import AcademicLevel, Classes, StudentDepartment
from V2.app.core.curriculum.models.curriculum import StudentSubject
from V2.app.core.assessment.models.assessment import Grade, TotalGrade
from V2.app.core.progression.models.progression import Repetition, Promotion, Graduation
from V2.app.core.transfer.models.transfer import StudentDepartmentTransfer, ClassTransfer
