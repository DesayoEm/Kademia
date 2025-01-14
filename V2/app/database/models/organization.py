from .common_imports import *
from mixins import AuditMixins, SoftDeleteMixins, TimeStampMixins
from app.database.models.data_enums import (
    DepartmentType, DepartmentCode,
    ClassLevel, ClassCode, StaffDepartmentName)

class Departments(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'departments'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    name: Mapped[DepartmentType] = mapped_column(Enum(DepartmentType))
    code: Mapped[DepartmentCode] = mapped_column(Enum(DepartmentCode))
    description: Mapped[str] = mapped_column(String(500))
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id', ondelete='SET NULL'), nullable = True)

    #Relationships
    students = relationship('Students', back_populates='department')
    mentor = relationship('Educator', back_populates='mentored_department', foreign_keys=[mentor_id])



class Classes(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'classes'

    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    level: Mapped[ClassLevel] = mapped_column(Enum(ClassLevel), primary_key=True)
    code: Mapped[ClassCode] = mapped_column(Enum(ClassCode), primary_key=True)
    mentor_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id', ondelete='SET NULL'), nullable=True)

    #Relationships
    students = relationship('Students', back_populates='class_')
    mentor = relationship('Staff', back_populates='mentored_class', foreign_keys=[mentor_id])

    def __repr__(self) -> str:
        return f"Class(level={self.level}, code={self.code}, mentor={self.mentor_id})"



class StaffDepartments(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'staff_departments'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    name: Mapped[StaffDepartmentName] = mapped_column(Enum(StaffDepartmentName), primary_key=True)
    description: Mapped[str] = mapped_column(String(500))
    manager_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id',ondelete='SET NULL'))


    #Relationships
    manager = relationship('Staff', back_populates='department_led', foreign_keys = [manager_id])


class StaffRoles(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    __tablename__ = 'staff_roles'
    id: Mapped[UUID]  = mapped_column(UUID(as_uuid = True), primary_key= True, default = uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(String(500), unique=True)






