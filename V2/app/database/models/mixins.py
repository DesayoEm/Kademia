from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from .enums import ArchiveReason
from sqlalchemy import Enum


class TimeStampMixins:
    """
    Provides timestamp attributes for tracking creation and modification times.
    Attributes:
        created_at (datetime): Timestamp when the record is created.
        last_modified_at (datetime): Timestamp when the record was last modified.
    """
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    last_modified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,
                                                       default=func.now(), onupdate=func.now())


class AuditMixins:
    """
    Provides audit attributes for tracking the users who created and last modified a record.
    Attributes:
        created_by (UUID): ID of the users who created the record.
        last_modified_by (UUID): ID of the users who last modified the record.
    """
    @declared_attr
    def created_by(cls):
        return mapped_column(ForeignKey('staff.id',ondelete='SET NULL',
            name=f'fk_{cls.__tablename__}_staff_created_by'),nullable=False
        )

    @declared_attr
    def last_modified_by(cls):
        return mapped_column(
            ForeignKey('staff.id',ondelete='RESTRICT',
            name=f'fk_{cls.__tablename__}_staff_last_modified_by'),nullable=False
        )

    @declared_attr
    def created_by_staff(cls):
        return relationship( 'Staff',uselist=False,
        foreign_keys=[cls.created_by], primaryjoin=f"Staff.id == {cls.__name__}.created_by"
        )

    @declared_attr
    def last_modified_by_staff(cls):
        return relationship(
            'Staff',uselist=False,
            foreign_keys=[cls.last_modified_by], primaryjoin=f"Staff.id == {cls.__name__}.last_modified_by"
        )


class ArchiveMixins:
    """
    Provides archive functionality for marking records as deleted without removing them from the database.

    Attributes:
        is_archived (bool): Indicates whether the record is archived.
        archived_at (datetime): Timestamp when the record was archived.
        archive_reason (ArchiveReason): Reason for the soft deletion.
        archived_by (UUID): ID of the staff member who performed the archive.
        archived_by_staff (relationship): Relationship to the staff member who deleted the record.

    Methods:
        archive (archived_by, reason): Marks the instance as archived.
    """
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    archived_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    archive_reason: Mapped[ArchiveReason] = mapped_column(Enum(ArchiveReason), nullable=True)

    @declared_attr
    def archived_by(cls):
        return mapped_column(
            ForeignKey('staff.id',ondelete='SET NULL',
                name=f'fk_{cls.__tablename__}_staff_archived_by'
                ),nullable=True
            )

    @declared_attr
    def archived_by_staff(cls):
        return relationship(
            'Staff',uselist=False,
            foreign_keys=[cls.archived_by],
            primaryjoin=f"Staff.id == {cls.__name__}.archived_by"
        )

    def archive(self, archived_by: UUID, archive_reason: ArchiveReason) -> None:
        """Marks the instance as archived."""
        self.is_archived = True
        self.archived_at = datetime.now(timezone.utc)
        self.archived_by = archived_by
        self.archive_reason = archive_reason

    def restore(self) -> None:
        """Restores an archived entity"""
        self.is_archived = False
