from V2.app.database.models.common_imports import *
from V2.app.database.models.data_enums import StaffType, Gender, UserType, AccessLevel
from V2.app.database.models.mixins import AuditMixins, SoftDeleteMixins, TimeStampMixins
from sqlalchemy.orm import declared_attr

class ProfileBase(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    """
   Abstract base class for user profiles, including personal details, activity status, and eligibility for deletion.

   Inherits from Base, AuditMixins, TimeStampMixins, and SoftDeleteMixins.
   """
    __abstract__ = True

    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    password_hash: Mapped[str] = mapped_column(String(300))

    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    gender: Mapped[str] = mapped_column(Enum(Gender, values_callable=lambda obj: [e.value for e in obj]))
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    deletion_eligible: Mapped[bool] = mapped_column(Boolean, default=False)


class Students(ProfileBase):
    """
    Represents a student, including personal details, enrollment information, academic status, and relationships with other entities.

    Inherits from ProfileBase.
    Relationships:
        - documents_owned (StudentDocuments): The student's owned documents.
        - parent (Parents): The student's parent or guardian.
        - class_ (Classes): The class the student belongs to.
        - department (Departments): The department the student belongs to.
        - subjects_taken (StudentSubjects): Subjects the student is enrolled in.
        - grades (Grades): Grades associated with the student.
        - total_grades (TotalGrades): Total grades for the student.
        - classes_repeated (Repetitions): Classes the student has repeated.
        - transfers (StudentTransfers): Transfers related to the student.
    """
    __tablename__ = 'students'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel, values_callable=lambda obj: [e.value for e in obj]), default = AccessLevel.USER)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType, values_callable=lambda obj: [e.value for e in obj]), default = UserType.STUDENT)
    image_url: Mapped[str] = mapped_column(String(200), nullable=True)
    student_id: Mapped[str] = mapped_column(String(20), unique=True)
    class_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('classes.id', ondelete='RESTRICT'))
    department_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('departments.id', ondelete='RESTRICT'))
    parent_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('parents.id', ondelete='RESTRICT'))
    is_repeating: Mapped[bool] = mapped_column(Boolean, default=False)
    admission_date: Mapped[date] = mapped_column(Date)
    leaving_date: Mapped[date] = mapped_column(Date, nullable=True)
    is_graduated: Mapped[bool] = mapped_column(Boolean, default=False)
    graduation_date: Mapped[date] = mapped_column(Date, nullable=True)
    is_enrolled: Mapped[bool] = mapped_column(Boolean, default=True)

    #Relationships
    documents_owned = relationship('StudentDocuments', back_populates='owner')
    parent = relationship('Parents', back_populates='wards',foreign_keys='[Students.parent_id]' )
    class_ = relationship('Classes', back_populates='students', foreign_keys='[Students.class_id]')
    department = relationship('Departments', back_populates='students', foreign_keys='[Students.department_id]')
    subjects_taken = relationship('StudentSubjects', back_populates='student')
    grades = relationship('Grades', back_populates='student')
    total_grades = relationship('TotalGrades', back_populates='student')
    classes_repeated = relationship('Repetitions', back_populates='repeater')
    transfers = relationship('StudentTransfers', back_populates='transferred_student')

    __table_args__ = (
        Index('idx_students_soft_deleted_at', 'soft_deleted_at'),
    )

    def __repr__(self) -> str:
        return f"Student(name={self.first_name} {self.last_name}, class={self.class_id})"


class Parents(ProfileBase):
    """
   Represents a parent or guardian of students, including contact information and relationship with the students they oversee.
   Inherits from ProfileBase.

   Relationships:
       - wards (Students): The students under the parent's guardianship.
   """
    __tablename__ = 'parents'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel, values_callable=lambda obj: [e.value for e in obj]), default = AccessLevel.USER)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType, values_callable=lambda obj: [e.value for e in obj]), default = UserType.PARENT)
    image_url: Mapped[str] = mapped_column(String(200), nullable=True)
    email_address: Mapped[str] = mapped_column(String(255), unique=True)
    address: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(11), unique=True)
    has_active_wards: Mapped[bool] = mapped_column(Boolean, default=True)

    #Relationships
    wards = relationship('Students', back_populates='parent')

    __table_args__ = (
        Index('idx_parents_email', 'email_address'),
        Index('idx_parents_phone', 'phone'),
        Index('idx_parents_soft_deleted_at', 'soft_deleted_at'),
    )

    def __repr__(self) -> str:
        return f"Parent(name={self.first_name} {self.last_name}, phone={self.phone})"


class Staff(ProfileBase):
    """
    Represents a staff member, including personal details, role, department, and employment status.

    Inherits from ProfileBase.
    Relationships:
        - department (StaffDepartments): The department the staff member belongs to.
        - role (StaffRoles): The role or position the staff member holds.
    """
    __tablename__ = 'staff'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel, values_callable=lambda obj: [e.value for e in obj]), default = AccessLevel.ADMIN)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType, values_callable=lambda obj: [e.value for e in obj]), default = UserType.STAFF)
    staff_type: Mapped[StaffType] = mapped_column(Enum(StaffType,values_callable=lambda obj: [e.value for e in obj]))
    image_url: Mapped[str] = mapped_column(String(200))
    email_address: Mapped[str] = mapped_column(String(255), unique=True)
    address: Mapped[str] = mapped_column(String(500))
    phone: Mapped[str] = mapped_column(String(11), unique=True)
    department_id: Mapped[UUID] = mapped_column(ForeignKey('staff_departments.id', ondelete='RESTRICT'))
    role_id: Mapped[UUID] = mapped_column(ForeignKey('staff_roles.id', ondelete='CASCADE'))
    date_joined: Mapped[date] = mapped_column(Date)
    date_left: Mapped[date] = mapped_column(Date, nullable=True)

    #Relationships
    department = relationship("StaffDepartments", foreign_keys="[Staff.department_id]")
    role = relationship("StaffRoles", foreign_keys='[Staff.role_id]')
    access_changes = relationship('AccessLevelChanges', back_populates='user')

    __table_args__ = (
        Index('idx_staff_soft_deleted_at', 'soft_deleted_at'),
        Index('idx_staff_department', 'department_id'),
        Index('idx_staff_role', 'role_id'),
        Index('idx_staff_name', 'first_name', 'last_name')
    )

    def __repr__(self) -> str:
        return f"Staff(name={self.first_name} {self.last_name}, is_active={self.is_active})"

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
        'polymorphic_on': staff_type
    }


class Educator(Staff):
    """
    Represents an educator, inheriting from Staff.
    Relationships:
        - subjects_taken (EducatorSubjects): Subjects the educator is responsible for.
        - mentored_department (Departments): The department the educator mentors.
        - mentored_class (Classes): The class level the educator mentors.
    """
    __tablename__ = 'educator'

    id: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Educator',
        'inherit_condition': (id == Staff.id)
    }

    subjects_taken = relationship('EducatorSubjects', back_populates='educator')
    mentored_department = relationship("Departments", back_populates="mentor")
    mentored_class = relationship("Classes", back_populates="mentor")


    def __repr__(self) -> str:
        return f"Educator(name ={self.first_name} {self.last_name})"


class Operations(Staff):
    """
    Represents an operations staff member, inheriting from Staff.
    """
    __tablename__ = 'operations'

    id: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Operations',
        'inherit_condition': (id == Staff.id)
    }

    def __repr__(self) -> str:
        return f"Operations staff(name ={self.first_name} {self.last_name}, role_id={self.role_id})"


class Support(Staff):
    """
     Represents a support staff member, inheriting from Staff.
    """
    __tablename__ = 'support'

    id: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'Support',
        'inherit_condition': (id == Staff.id)
    }

    def __repr__(self) -> str:
        return f"Support staff(name ={self.first_name} {self.last_name}, role_id={self.role_id})"

class System(Staff):
    """
     Represents the system, inheriting from Staff.
    """
    __tablename__ = 'system'

    id: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'System',
        'inherit_condition': (id == Staff.id)
    }

    def __repr__(self) -> str:
        return f"System(name={self.first_name} {self.last_name}, role_id={self.role_id})"