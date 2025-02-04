from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID


class TimeStampMixins:
    """
     Provides timestamp attributes for tracking creation and modification times.
     Attributes:
         created_at (datetime): Timestamp when the record is created.
         last_modified_at (datetime): Timestamp when the record was last modified.
     """
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    last_modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())



class AuditMixins:
    """
   Provides audit attributes for tracking the user who created and last modified a record.
   Attributes:
       created_by (UUID): ID of the user who created the record.
       last_modified_by (UUID): ID of the user who last modified the record.
   """
    @declared_attr
    def created_by(cls):
        return mapped_column(ForeignKey('staff.id', ondelete= 'SET NULL'), nullable = True)

    @declared_attr
    def last_modified_by(cls):
        return mapped_column(ForeignKey('staff.id', ondelete= 'SET NULL'), nullable = True)

    @declared_attr
    def created_by_staff(cls):
        return relationship('Staff', uselist=False,foreign_keys=[cls.created_by],
                            primaryjoin=f"Staff.id == {cls.__name__}.created_by")

    @declared_attr
    def last_modified_by_staff(cls):
        return relationship('Staff', uselist=False,foreign_keys=[cls.last_modified_by],
                            primaryjoin=f"Staff.id == {cls.__name__}.last_modified_by")


class ArchiveMixins:
    """
     Provides archive functionality for marking records as deleted without removing them from the database.

    Attributes:
        is_archived (bool): Indicates whether the record is archived.
        archived_at (datetime): Timestamp when the record was archived.
        archive_reason (str | None): Reason for the soft deletion.
        archived_by (UUID): ID of the staff member who performed the archive.
        archived_by_staff (relationship): Relationship to the staff member who deleted the record.

    Methods:
        archive (archived_by, reason): Marks the instance as archived.
    """
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    archived_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    archive_reason: Mapped[str | None] = mapped_column(String(500), nullable = True)

    @declared_attr
    def archived_by(cls):
        return mapped_column(ForeignKey('staff.id', ondelete= 'SET NULL'), nullable = True)

    @declared_attr
    def archived_by_staff(cls):
        return relationship('Staff', uselist=False, foreign_keys=[cls.archived_by],
                            primaryjoin=f"Staff.id == {cls.__name__}.archived_by")

    def archive(self, arvhived_by: UUID, reason: str | None = None) -> None:
        """Marks the instance as archived."""
        self.is_archived = True
        self.archived_at = datetime.now(timezone.utc)
        self.archived_by = arvhived_by
        self.archive_reason = reason