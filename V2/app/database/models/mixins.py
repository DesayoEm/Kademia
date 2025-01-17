from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, DateTime, String, func
from datetime import datetime
import uuid


class TimeStampMixins:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    last_modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )


class AuditMixins:
    @declared_attr
    def created_by(cls) -> Mapped[uuid.UUID]:
        return mapped_column(UUID(as_uuid=True), default=uuid.uuid4)

    @declared_attr
    def last_modified_by(cls) -> Mapped[uuid.UUID]:
        return mapped_column(UUID(as_uuid=True), default=uuid.uuid4)


class SoftDeleteMixins:
    is_soft_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    soft_deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    deletion_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)

    @declared_attr
    def soft_deleted_by(cls) -> Mapped[uuid.UUID]:
        return mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
