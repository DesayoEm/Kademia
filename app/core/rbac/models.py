
from app.core.shared.models.common_imports import *
from app.core.shared.models.enums import Resource, Action, UserRoleName
from app.core.shared.models.mixins import AuditMixins, TimeStampMixins, ArchiveMixins


class Permission(Base, AuditMixins, TimeStampMixins):
    """Represents a specific permission (resource + action)"""
    __tablename__ = 'permissions'

    name: Mapped[str] = mapped_column(String(50))
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    resource: Mapped[Resource] = mapped_column(Enum(Resource, name='resource'))
    action: Mapped[Action] = mapped_column(Enum(Action, name ='action'))
    description: Mapped[str] = mapped_column(String(200), nullable=True)

    roles: Mapped[List['Role']] = relationship(
        secondary='role_permissions', back_populates='permissions'
    )


class Role(Base,TimeStampMixins, ArchiveMixins):
    """Represents a role that can be assigned to users"""
    __tablename__ = 'roles'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[UserRoleName] = mapped_column(Enum(UserRoleName, name='userrolename'), unique=True)
    description: Mapped[str] = mapped_column(String(3000))
    rank: Mapped[int] = mapped_column(Integer)

    #Audit
    created_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=True)
    last_modified_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=True)

    #relationships
    permissions: Mapped[List['Permission']] = relationship(
        secondary='role_permissions', back_populates='roles'
    )

    staff: Mapped[List['Staff']] = relationship(back_populates='role')#on staff only


class RolePermission(Base):
    __tablename__ = 'role_permissions'

    role_id: Mapped[UUID] = mapped_column(ForeignKey('roles.id'), primary_key=True)
    permission_id: Mapped[UUID] = mapped_column(ForeignKey('permissions.id'), primary_key=True)


class RoleHistory(Base, ArchiveMixins):
    """Tracks role changes for staff members over time"""
    __tablename__ = 'role_history'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    staff_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id', ondelete='CASCADE'))
    previous_role_id: Mapped[UUID] = mapped_column(ForeignKey('roles.id', ondelete='RESTRICT'), nullable=True)
    new_role_id: Mapped[UUID] = mapped_column(ForeignKey('roles.id', ondelete='RESTRICT'))
    change_reason: Mapped[str] = mapped_column(String(500))

    # Audit fields
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    changed_by_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id', ondelete='RESTRICT'))
    effective_from: Mapped[date] = mapped_column(Date(), default=func.now())
    effective_until: Mapped[date] = mapped_column(Date(), nullable=True)

    # Relationships
    staff_member: Mapped['Staff'] = relationship('Staff', foreign_keys='[RoleHistory.staff_id]', back_populates='role_changes')
    changed_by: Mapped['Staff'] = relationship('Staff', foreign_keys='[RoleHistory.changed_by_id]')


    __table_args__ = (
        Index('idx_staff_role_history_staff', 'staff_id'),
        Index('idx_staff_role_history_dates', 'staff_id', 'effective_from', 'effective_until'),
        Index('idx_staff_role_history_current', 'staff_id', 'effective_until'),
    )


from app.core.identity.models.staff import Staff
from app.core.shared.models.mixins import ArchiveMixins
