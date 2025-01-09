from base import *
from validators import StaffType,Gender

class Students(Base):
    __tablename__ = 'students'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    student_id: Mapped[str] = mapped_column(String(20), unique = True, Nullable = False)
    first_name: Mapped[str] = mapped_column(String(30), nullable = False)
    last_name: Mapped[str] = mapped_column(String(30), nullable = False)
    gender: Mapped[str] = mapped_column(Enum(Gender), nullable = False)
    class_id: Mapped[str] = mapped_column(String(1), ForeignKey('classes.id'), nullable= False)
    department_id: Mapped[UUID] = mapped_column(UUID(as_uuid =True), ForeignKey('departments.id'), nullable= False)
    parent_id: Mapped[UUID] = mapped_column(UUID(as_uuid = True), ForeignKey('parents.id'), nullable= False)
    image_url: Mapped[str] = mapped_column(String(200), nullable = False)
    is_repeating: Mapped[bool] = mapped_column(Boolean, default = False, Nullable = False)
    admission_date: Mapped[date] = mapped_column(Date, nullable = False)
    leaving_date: Mapped[date] = mapped_column(Date)
    is_graduated: Mapped[bool] = mapped_column(Boolean, default = False)
    graduation_date: Mapped[date] = mapped_column(Date)
    is_enrolled: Mapped[bool] = mapped_column(Boolean, default = True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable= False)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(),onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'))

    #Relationships
    parent = relationship('Parents', back_populates = 'wards')
    class_ = relationship('Classes', back_populates = 'students')
    departments = relationship('Departments', back_populates='students')
    created_by_staff = relationship("Staff", foreign_keys=[created_by])
    updated_by_staff = relationship("Staff", foreign_keys=[updated_by])


    def __repr__(self) -> str:
        return f"Student(id={self.student_id}, name={self.first_name} {self.last_name}, class={self.class_id})"


class Parents(Base):
    __tablename__ = 'parents'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    first_name: Mapped[str] = mapped_column(String(30), nullable = False)
    last_name: Mapped[str] = mapped_column(String(30), nullable = False)
    email_address: Mapped[str] = mapped_column(String(255), nullable = False)
    address: Mapped[str] = mapped_column(String(255), nullable = False)
    phone: Mapped[str] = mapped_column(String(11), nullable = False)
    has_active_wards: Mapped[bool] = mapped_column(Boolean, default = True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable= False)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(),onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'))

    #Relationships
    wards = relationship('Students', back_populates='parent')
    created_by_staff = relationship("Staff", foreign_keys=[created_by])
    updated_by_staff = relationship("Staff", foreign_keys=[updated_by])

    def __repr__(self) -> str:
        return f"Parent(name={self.first_name} {self.last_name}, phone={self.phone})"



class Staff(Base):
    __tablename__ = 'staff'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    first_name: Mapped[str] = mapped_column(String(30), nullable = False)
    last_name: Mapped[str] = mapped_column(String(30), nullable = False)
    email_address: Mapped[str] = mapped_column(String(255), nullable = False)
    address: Mapped[str] = mapped_column(String(500), nullable = False)
    phone: Mapped[str] = mapped_column(String(11), nullable = False)
    role: Mapped [str] = mapped_column (String (100), nullable = False)
    role_description: Mapped [str] = mapped_column (String (500), nullable = False)
    date_joined: Mapped[date] = mapped_column(Date, nullable = False)
    date_left: Mapped[date] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default = True)
    staff_type: Mapped[StaffType] = mapped_column(Enum(StaffType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable= False)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(),onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'))

    #Relationships
    created_records = relationship('Students', foreign_keys=[Students.created_by], back_populates="created_by_staff")
    updated_records = relationship("Students", foreign_keys=[Students.updated_by], back_populates="updated_by_staff")
    created_by_staff = relationship("Staff", foreign_keys=[created_by])
    updated_by_staff = relationship("Staff", foreign_keys=[updated_by])


    def __repr__(self) -> str:
        return f"Staff(name={self.first_name} {self.last_name}, is_active={self.is_active})"

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
        'polymorphic_on': staff_type
    }


class Admin(Staff):
    __tablename__ = 'admin'
    id: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), primary_key=True)
    department_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('staff_departments.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __repr__(self) -> str:
        return f"Admin(name={self.first_name} {self.last_name}, role={self.role})"


class Educator(Staff):
    __tablename__ = 'educator'

    id: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), primary_key=True)
    department_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey('staff_departments.id'))
    subject_taught: Mapped[str] = mapped_column(String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'educator',
    }

    def __repr__(self) -> str:
        return f"Educator(name ={self.first_name} {self.last_name}, role={self.role})"







