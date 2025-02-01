from .common_imports import *
from .data_enums import AccessLevel
from .mixins import AuditMixins, SoftDeleteMixins, TimeStampMixins

class AccessLevelChanges(Base, TimeStampMixins):
    """Tracks changes to user access levels for audit purposes"""
    __tablename__ = 'access_level_changes'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    staff_id: Mapped[UUID] = mapped_column(ForeignKey('staff.id', ondelete='CASCADE'))
    previous_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel))
    new_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel))
    reason: Mapped[str] = mapped_column(String(500))

    #Audit
    changed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=func.now())
    changed_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id', ondelete='SET NULL'))

    #Relationships
    user: Mapped['Staff'] = relationship(back_populates='access_changes', foreign_keys="[AccessLevelChanges.staff_id]")

    def __repr__(self) -> str:
        return f"AccessChange(user={self.staff_id}, {self.previous_level}->{self.new_level})"