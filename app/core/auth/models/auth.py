from app.core.shared.models.common_imports import *
from app.core.shared.models.enums import AccessLevel
from app.core.shared.models.mixins import ArchiveMixins


class AccessLevelChange(Base, ArchiveMixins):
    """Tracks changes to users access levels for audit purposes"""
    __tablename__ = 'access_level_changes'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    staff_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id',
            ondelete='CASCADE',name='fk_access_level_changes_staff_staff_id')
        )
    previous_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel, name='accesslevel'))
    new_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel, name='accesslevel'))
    reason: Mapped[str] = mapped_column(String(500))

    # Audit
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    changed_by_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id',
            ondelete='RESTRICT',name='fk_access_level_changes_staff_changed_by')
        )

    # Relationships
    user: Mapped['Staff'] = relationship(back_populates='access_changes',
            foreign_keys="[AccessLevelChange.staff_id]", passive_deletes=True)

    __table_args__ = (
        Index('idx_staff_id', 'staff_id'),
        Index('idx_access_level_changed_by', 'changed_by_id'),
    )


    def __repr__(self) -> str:
        return f"AccessChange(user={self.staff_id}, {self.previous_level}->{self.new_level})"

