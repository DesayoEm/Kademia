from app.core.shared.models.common_imports import *
from app.core.shared.models.enums import Resource, Action, UserRoleName
from app.core.shared.models.mixins import AuditMixins, TimeStampMixins, ArchiveMixins


"""
Role-Based Access Control (RBAC) models for the authorization system.

Implements a permission model where:
- Permissions define granular access rights (resource + action combinations)
- Roles group permissions together for assignment to users
- RoleHistory tracks staff role changes over time for audit purposes

The many-to-many relationship between Role and Permission is managed through
the RolePermission association table.
"""



class Permission(Base, AuditMixins, TimeStampMixins):
    """Represents a specific permission (resource + action)"""

    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String(50))
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    resource: Mapped[Resource] = mapped_column(Enum(Resource, name="resource"))
    action: Mapped[Action] = mapped_column(Enum(Action, name="action"))
    description: Mapped[str] = mapped_column(String(200), nullable=True)

    roles: Mapped[List["Role"]] = relationship(
        secondary="role_permissions", back_populates="permissions"
    )


class Role(Base, TimeStampMixins, ArchiveMixins):
    """Represents a role that can be assigned to users"""

    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[UserRoleName] = mapped_column(
        Enum(UserRoleName, name="userrolename"), unique=True
    )
    description: Mapped[str] = mapped_column(String(3000))
    rank: Mapped[int] = mapped_column(Integer, nullable=True)

    # Audit
    created_by: Mapped[UUID] = mapped_column(ForeignKey("staff.id"), nullable=True)
    last_modified_by: Mapped[UUID] = mapped_column(
        ForeignKey("staff.id"), nullable=True
    )

    # relationships
    permissions: Mapped[List["Permission"]] = relationship(
        secondary="role_permissions", back_populates="roles"
    )

    staff_members: Mapped[List["Staff"]] = relationship(
        back_populates="role", primaryjoin="Staff.current_role_id == Role.id"
    )  # on staff only


class RolePermission(Base, AuditMixins, TimeStampMixins):
    __tablename__ = "role_permissions"

    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    permission_id: Mapped[UUID] = mapped_column(
        ForeignKey("permissions.id"), primary_key=True
    )


class RoleHistory(Base, ArchiveMixins):
    """
    Audit log tracking role changes for staff members over time.

    Creates a complete history of role assignments, enabling queries like
    "what role did this person have on date X?" and "who approved this change?".
    Supports effective dating for scheduled role changes.

    Attributes:
        id: Primary key UUID.
        staff_id: The staff member whose role changed.
        previous_role_id: The role before the change (nullable for initial assignment).
        new_role_id: The role after the change.
        change_reason: Required explanation for the role change.
        changed_at: Timestamp when the change record was created.
        changed_by_id: Staff member who authorized/made the change.
        effective_from: Date the new role takes effect.
        effective_until: Date the role assignment ended (null if current).
        staff_member: Relationship to the affected Staff object.
        changed_by: Relationship to the Staff who made the change.

    Indexes:
        idx_staff_role_history_staff: Fast lookup by staff_id.
        idx_staff_role_history_dates: Supports date-range queries per staff.
        idx_staff_role_history_current: Optimizes "current role" lookups
            (where effective_until IS NULL).

    Mixins:
        ArchiveMixins: Supports soft-delete of history records.
    """

    __tablename__ = "role_history"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    staff_id: Mapped[UUID] = mapped_column(ForeignKey("staff.id", ondelete="CASCADE"))
    previous_role_id: Mapped[UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="RESTRICT"), nullable=True
    )
    new_role_id: Mapped[UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="RESTRICT")
    )
    change_reason: Mapped[str] = mapped_column(String(500))

    # Audit fields
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    changed_by_id: Mapped[UUID] = mapped_column(
        ForeignKey("staff.id", ondelete="RESTRICT")
    )
    effective_from: Mapped[date] = mapped_column(Date(), default=func.now())
    effective_until: Mapped[date] = mapped_column(Date(), nullable=True)

    # Relationships
    staff_member: Mapped["Staff"] = relationship(
        "Staff", foreign_keys="[RoleHistory.staff_id]", back_populates="role_changes"
    )
    changed_by: Mapped["Staff"] = relationship(
        "Staff", foreign_keys="[RoleHistory.changed_by_id]"
    )

    __table_args__ = (
        Index("idx_staff_role_history_staff", "staff_id"),
        Index(
            "idx_staff_role_history_dates",
            "staff_id",
            "effective_from",
            "effective_until",
        ),
        Index("idx_staff_role_history_current", "staff_id", "effective_until"),
    )


from app.core.identity.models.staff import Staff
from app.core.shared.models.mixins import ArchiveMixins
