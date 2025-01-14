from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID


class TimeStampMixins:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())



class AuditMixins:
    @declared_attr
    def created_by(cls):
        return mapped_column(ForeignKey('staff.id', ondelete= 'SET NULL'), nullable = True)

    @declared_attr
    def updated_by(cls):
        return mapped_column(ForeignKey('staff.id', ondelete= 'SET NULL'), nullable = True)

    @declared_attr
    def created_by_staff(cls):
        return relationship('Staff', backref="created_records", uselist=False, foreign_keys=[cls.created_by])

    @declared_attr
    def updated_by_staff(cls):
        return relationship('Staff', backref="updated_records", uselist=False, foreign_keys=[cls.updated_by])


class SoftDeleteMixins:
    is_soft_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    deletion_reason: Mapped[str | None] = mapped_column(String(500), nullable = True)

    @declared_attr
    def soft_deleted_by(cls):
        return mapped_column(ForeignKey('staff.id', ondelete= 'SET NULL'), nullable = True)

    @declared_attr
    def soft_deleted_by_staff(cls):
        return relationship('Staff', backref="soft_deleted_records", uselist=False, foreign_keys=[cls.soft_deleted_by])

    def soft_delete(self, deleted_by: UUID, reason: str | None = None) -> None:
        """Marks the instance as soft-deleted."""
        self.is_soft_deleted = True
        self.deleted_at = datetime.now(timezone.utc)
        self.deleted_by = deleted_by
        self.deletion_reason = reason
