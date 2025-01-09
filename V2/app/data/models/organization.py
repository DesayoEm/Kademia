from base import *
from validators import DepartmentType, DepartmentCode, ClassLevel, ClassCode, StaffDepartmentName

class Departments(Base):
    __tablename__ = 'departments'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    name: Mapped[DepartmentType] = mapped_column(Enum(DepartmentType), nullable=False)
    code: Mapped[DepartmentCode] = mapped_column(Enum(DepartmentCode), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable = True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)

    #Relationships
    students = relationship('Students', back_populates='department')
    mentor = relationship('Staff', back_populates='mentees')
    creator = relationship('Staff', foreign_keys = [created_by])
    updater = relationship('Staff', foreign_keys = [updated_by])


class Classes(Base):
    __tablename__ = 'classes'

    level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel), primary_key=True)
    code: Mapped[ClassCode] = mapped_column(Enum(ClassCode), primary_key=True)
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('level', 'code'),
    )

    #Relationships
    students = relationship('Students', back_populates='class_')
    mentor = relationship('Staff', back_populates='mentored_class', foreign_keys=[mentor_id])
    creator = relationship('Staff', foreign_keys=[created_by])
    updater = relationship('Staff', foreign_keys=[updated_by])

    def __repr__(self) -> str:
        return f"Class(level={self.level}, code={self.code}, mentor={self.mentor_id})"


class StaffDepartments(Base):
    __tablename__ = 'staff_departments'
    name: Mapped[StaffDepartmentName] = mapped_column(Enum(StaffDepartmentName), primary_key=True)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    manager_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)

    #Relationships
    staff = relationship('Staff', back_populates='department')
    creator = relationship('Staff', foreign_keys = [created_by])
    updater = relationship('Staff', foreign_keys = [updated_by])





