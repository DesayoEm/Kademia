from app.database.models.common_imports import *
from app.database.models.mixins import AuditMixins, SoftDeleteMixins, TimeStampMixins
from app.database.models.data_enums import (
    DepartmentType, DepartmentCode,
    ClassLevel, ClassCode, StaffDepartmentName)

class Departments(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'departments'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    name: Mapped[DepartmentType] = mapped_column(Enum(DepartmentType))
    code: Mapped[DepartmentCode] = mapped_column(Enum(DepartmentCode))
    description: Mapped[str] = mapped_column(String(500))
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey('educator.id', ondelete='SET NULL'), nullable = True)

    #Relationships
    students = relationship('Students', back_populates='department')
    mentor = relationship('Educator', back_populates='mentored_department', foreign_keys='[Departments.mentor_id]')



class Classes(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'classes'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel))
    code: Mapped[ClassCode] = mapped_column(Enum(ClassCode))
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey('educator.id', ondelete='SET NULL'), nullable=True)

    #Relationships
    students = relationship('Students', back_populates='class_')
    mentor = relationship('Educator', back_populates='mentored_class', foreign_keys='[Classes.mentor_id]')

    __table_args__ = (
        UniqueConstraint('level', 'code', name='uq_class_level_code'),
        Index('idx_class_level_code', 'level', 'code')
    )

    def __repr__(self) -> str:
        return f"Class(level={self.level}, code={self.code}, mentor={self.mentor_id})"



class StaffDepartments(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'staff_departments'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    name: Mapped[StaffDepartmentName] = mapped_column(Enum(StaffDepartmentName), unique=True)
    description: Mapped[str] = mapped_column(String(500))
    manager_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id',ondelete='SET NULL'), nullable = True)


    #Relationships
    manager = relationship('Staff', foreign_keys = '[StaffDepartments.manager_id]')


class StaffRoles(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'staff_roles'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(500), unique=True)






