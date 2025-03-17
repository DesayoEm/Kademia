from .common_imports import *
from .data_enums import StaffType, Gender, UserType, AccessLevel, StudentStatus, StaffAvailability, EmploymentStatus
from .mixins import AuditMixins, TimeStampMixins, ArchiveMixins


class ProfileBase(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Abstract base class for users profiles, including personal details, activity status, and eligibility for deletion.
    Inherits from Base, AuditMixins, TimeStampMixins, and SoftDeleteMixins.
    """
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    password_hash: Mapped[str] = mapped_column(String(300))
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    gender: Mapped[Gender] = mapped_column(Enum(Gender, name="gender"))
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    deletion_eligible: Mapped[bool] = mapped_column(Boolean, default=False)


class Students(ProfileBase):
    """
    Represents a student, including personal details, enrollment information, academic status, and relationships with other entities.
    Inherits from ProfileBase.
    """
    __tablename__ = 'students'

    student_id: Mapped[str] = mapped_column(String(14), unique=True)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType, name='usertype'), default=UserType.STUDENT)
    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel, name='accesslevel'), default=AccessLevel.READ)
    status: Mapped[StudentStatus] = mapped_column(Enum(StudentStatus, name='studentstatus'), default=StudentStatus.ENROLLED)
    date_of_birth: Mapped[date] = mapped_column(Date)
    image_url: Mapped[str] = mapped_column(String(200), nullable=True)
    class_id: Mapped[UUID] = mapped_column(UUID,ForeignKey('classes.id',
            ondelete='RESTRICT',name='fk_students_classes_class_id')
        )
    level_id: Mapped[UUID] = mapped_column(UUID,ForeignKey('academic_levels.id',
            ondelete='RESTRICT',name='fk_students_academic_levels_level_id')
        )
    department_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),ForeignKey('student_departments.id',
            ondelete='RESTRICT',name='fk_students_student_departments_department_id')
        )
    guardian_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True),ForeignKey('guardians.id',
            ondelete='RESTRICT',name='fk_students_parents_parent_id')
        )
    is_repeating: Mapped[bool] = mapped_column(Boolean, default=False)
    admission_date: Mapped[date] = mapped_column(Date)
    date_left: Mapped[date] = mapped_column(Date, nullable=True)
    graduation_date: Mapped[date] = mapped_column(Date, nullable=True)

    # Relationships
    documents_owned: Mapped[List['StudentDocuments']] = relationship(back_populates='owner')
    awards_earned: Mapped[List['StudentAwards']] = relationship(back_populates='owner')
    guardian: Mapped['Guardians'] = relationship(back_populates='wards', foreign_keys='[Students.guardian_id]')
    class_: Mapped['Classes'] = relationship(back_populates='students',foreign_keys='[Students.class_id]',
        primaryjoin='Students.class_id == Classes.id')
    department: Mapped['StudentDepartments'] = relationship(back_populates='students', foreign_keys='[Students.department_id]')
    level: Mapped['AcademicLevel'] = relationship(back_populates='students', foreign_keys='[Students.level_id]')
    subjects_taken: Mapped[List['StudentSubjects']] = relationship(back_populates='student')
    grades: Mapped[List['Grades']] = relationship(back_populates='student')
    total_grades: Mapped[List['TotalGrades']] = relationship(back_populates='student')
    classes_repeated: Mapped[List['StudentRepetitions']] = relationship(back_populates='repeating_student')
    department_transfers: Mapped[List['StudentDepartmentTransfers']] = relationship(back_populates='transferred_student')
    class_transfers: Mapped[List['StudentClassTransfers']] = relationship(back_populates='transferred_student')

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


class Guardians(ProfileBase):
    """
    Represents a parent or guardian of students, including contact information and relationship with the students they oversee.
    Inherits from ProfileBase.
    """
    __tablename__ = 'guardians'

    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel, name='accesslevel'), default=AccessLevel.READ)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType, name='usertype'), default=UserType.GUARDIAN)
    image_url: Mapped[str] = mapped_column(String(225), nullable=True)
    email_address: Mapped[str] = mapped_column(String(255), unique=True)
    address: Mapped[str] = mapped_column(String(500))
    phone: Mapped[str] = mapped_column(String(14), unique=True)

    # Relationships
    wards: Mapped[List['Students']] = relationship(back_populates='guardian')

    __table_args__ = (
        Index('idx_guardians_name', 'first_name', 'last_name'),
        Index('idx_guardians_email', 'email_address'),
        Index('idx_guardians_phone', 'phone'),
        Index('idx_guardian_archived_at', 'archived_at'),
    )

    def __repr__(self) -> str:
        return f"Parent(name={self.first_name} {self.last_name}, phone={self.phone})"


class Staff(ProfileBase):
    """
    Represents a staff member, including personal details, role, department, and employment status.
    Inherits from ProfileBase.
    """
    __tablename__ = 'staff'

    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel, name='accesslevel'), default=AccessLevel.READ)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType, name='usertype'), default=UserType.STAFF)
    status: Mapped[EmploymentStatus] = mapped_column(Enum(EmploymentStatus, name='employmentstatus'), default=EmploymentStatus.ACTIVE)
    availability: Mapped[StaffAvailability] = mapped_column(Enum(StaffAvailability, name='staffavailability'), default=StaffAvailability.AVAILABLE)
    staff_type: Mapped[StaffType] = mapped_column(Enum(StaffType, name='stafftype'))
    image_url: Mapped[str] = mapped_column(String(200), nullable = True)
    email_address: Mapped[str] = mapped_column(String(255), unique=True)
    address: Mapped[str] = mapped_column(String(500))
    phone: Mapped[str] = mapped_column(String(14), unique=True)
    department_id: Mapped[UUID] = mapped_column(
        ForeignKey('staff_departments.id', ondelete='RESTRICT', name='fk_staff_staff_departments_department_id'),
        nullable=True
    )

    role_id: Mapped[UUID] = mapped_column(
        ForeignKey('staff_roles.id', ondelete='RESTRICT', name='fk_staff_staff_roles_role_id'),
        nullable=True)
    date_joined: Mapped[date] = mapped_column(Date)
    date_left: Mapped[date] = mapped_column(Date, nullable=True)

    # Relationships
    department: Mapped["StaffDepartments"] = relationship(back_populates='staff', foreign_keys="[Staff.department_id]")
    role: Mapped["StaffRoles"] = relationship(back_populates='staff', foreign_keys='[Staff.role_id]')
    access_changes: Mapped[List["AccessLevelChanges"]] = relationship(
        "AccessLevelChanges",
        back_populates='user',
        primaryjoin="Staff.id == AccessLevelChanges.staff_id"
    )

    __table_args__ = (
        Index('idx_staff_name', 'first_name', 'last_name'),
        Index('idx_staff_department', 'department_id'),
        Index('idx_staff_role', 'role_id'),
        Index('idx_staff_phone', 'phone')
    )

    def __repr__(self) -> str:
        return f"Staff(name={self.first_name} {self.last_name}, role={self.role_id})"

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
        'polymorphic_on': staff_type
    }


class Educator(Staff):
    """
    Represents an educator, inheriting from Staff.
    Relationships:
        - qualifications
        - subjects: Subjects the educator is responsible for.
        - mentored_department (Departments): The department the educator mentors.
        - mentored_class (Classes): The class level the educator mentors.
    """
    __tablename__ = 'educators'

    id: Mapped[UUID] = mapped_column(
        ForeignKey(
            'staff.id',
            name='fk_educators_staff_id'
        ),
        primary_key=True
    )

    __mapper_args__ = {
        'polymorphic_identity': 'Educator',
        'inherit_condition': (id == Staff.id)
    }

    qualifications: Mapped[List['EducatorQualifications']] = relationship(back_populates='educator')
    subject_assignments: Mapped[List['SubjectEducators']] = relationship(back_populates='teacher')
    mentored_department: Mapped[List['StudentDepartments']] = relationship(back_populates='mentor')
    mentored_class: Mapped['Classes'] = relationship(back_populates='mentor')

    def __repr__(self) -> str:
        return f"Educator(name={self.first_name} {self.last_name})"


class Operations(Staff):
    """
    Represents an operations staff member, inheriting from Staff.
    """
    __tablename__ = 'operations'

    id: Mapped[UUID] = mapped_column(ForeignKey('staff.id',
            name='fk_operations_staff_id'),primary_key=True
        )

    __mapper_args__ = {
        'polymorphic_identity': 'Operations',
        'inherit_condition': (id == Staff.id)
    }

    def __repr__(self) -> str:
        return f"Operations staff(name={self.first_name} {self.last_name}, role_id={self.role_id})"


class Support(Staff):
    """
    Represents a support staff member, inheriting from Staff.
    """
    __tablename__ = 'support'

    id: Mapped[UUID] = mapped_column(
        ForeignKey('staff.id',
            name='fk_support_staff_id'),primary_key=True
    )

    __mapper_args__ = {
        'polymorphic_identity': 'Support',
        'inherit_condition': (id == Staff.id)
    }

    def __repr__(self) -> str:
        return f"Support staff(name={self.first_name} {self.last_name}, role_id={self.role_id})"


class System(Staff):
    """
    Represents the system, inheriting from Staff.
    """
    __tablename__ = 'system'

    id: Mapped[UUID] = mapped_column(ForeignKey('staff.id',
            name='fk_system_staff_id'),primary_key=True
        )

    __mapper_args__ = {
        'polymorphic_identity': 'System',
        'inherit_condition': (id == Staff.id)
    }

    def __repr__(self) -> str:
        return f"System(name={self.first_name} {self.last_name}, role_id={self.role_id})"
