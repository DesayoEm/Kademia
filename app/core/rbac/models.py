
from app.core.shared.models.common_imports import *
from app.core.shared.models.enums import Resource, Action
from app.core.shared.models.mixins import AuditMixins, TimeStampMixins


class Permission(Base, AuditMixins, TimeStampMixins):
    """Represents a specific permission (resource + action)"""
    __tablename__ = 'permissions'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resource: Mapped[Resource] = mapped_column(Enum(Resource, name='resource'))
    action: Mapped[Action] = mapped_column(Enum(Action, name ='action'))
    description: Mapped[str] = mapped_column(String(200))

    roles: Mapped[List['Role']] = relationship(
        secondary='role_permissions', back_populates='permissions'
    )


class Role(Base, AuditMixins, TimeStampMixins):
    """Represents a role that can be assigned to users"""
    __tablename__ = 'roles'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(200))
    level: Mapped[int] = mapped_column(Integer)

    permissions: Mapped[List['Permission']] = relationship(
        secondary='role_permissions', back_populates='roles'
    )


class RolePermission(Base):
    """Many-to-many association table"""
    __tablename__ = 'role_permissions'

    role_id: Mapped[UUID] = mapped_column(ForeignKey('roles.id'), primary_key=True)
    permission_id: Mapped[UUID] = mapped_column(ForeignKey('permissions.id'), primary_key=True)


class StaffRole(Base, AuditMixins, TimeStampMixins):
    __tablename__ = 'staff_roles'
    staff_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), primary_key=True)
    role_id: Mapped[UUID] = mapped_column(ForeignKey('roles.id'), primary_key=True)
    assigned_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'))
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class StudentRole(Base, AuditMixins, TimeStampMixins):
    __tablename__ = 'student_roles'
    student_id: Mapped[UUID] = mapped_column(ForeignKey('students.id'), primary_key=True)
    role_id: Mapped[UUID] = mapped_column(ForeignKey('roles.id'), primary_key=True)
    assigned_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'))
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

class GuardianRole(Base, AuditMixins, TimeStampMixins):
    __tablename__ = 'guardian_roles'
    guardian_id: Mapped[UUID] = mapped_column(ForeignKey('guardians.id'), primary_key=True)
    role_id: Mapped[UUID] = mapped_column(ForeignKey('roles.id'), primary_key=True)
    assigned_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'))
    assigned_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())