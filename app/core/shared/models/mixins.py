from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from .enums import ArchiveReason
from sqlalchemy import Enum


class TimeStampMixins:
    """
    Provides timestamp attributes for tracking creation and modification times.

    Automatically manages created_at and last_modified_at fields for entities,
    using db functions to set appropriate timestamps.

    Attributes:
        created_at (datetime): Timestamp when the record is created.
        last_modified_at (datetime): Timestamp when the record was last modified.
                                     Automatically updates on record changes.
    """
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
        )

    last_modified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now(), onupdate=func.now()
    )


class AuditMixins:
    """
    Provides audit attributes for tracking the users who created and modified records.

    Establishes relationships to the Staff model for tracking who created and
    last modified each record. Foreign keys are configured with SET NULL to allow
    staff records to be deleted without affecting the audited entity.

    Attributes:
        created_by (UUID): ID of the staff member who created the record. Nullable.
        last_modified_by (UUID): ID of the staff member who last modified the record. Nullable.
        created_by_staff (Staff): Relationship to the staff member who created the record.
        last_modified_by_staff (Staff): Relationship to the staff member who modified the record.
    """

    @declared_attr
    def created_by(cls):
        return mapped_column(ForeignKey(
            'staff.id', ondelete='SET NULL',name=f'fk_{cls.__tablename__}_staff_created_by'),
                        nullable=False)

    @declared_attr
    def last_modified_by(cls):
        return mapped_column(ForeignKey(
            'staff.id', ondelete='SET NULL', name=f'fk_{cls.__tablename__}_staff_last_modified_by'),
                    nullable=False
        )

    @declared_attr
    def created_by_staff(cls):
        return relationship('Staff', foreign_keys=[cls.created_by],
                            primaryjoin=f"Staff.id == {cls.__name__}.created_by"
                )

    @declared_attr
    def last_modified_by_staff(cls):
        return relationship(
            'Staff', foreign_keys=[cls.last_modified_by],
                primaryjoin=f"Staff.id == {cls.__name__}.last_modified_by"
            )


class ArchiveMixins:
    """
    Provides archive functionality for soft deletion of records.
    Attributes:
        is_archived (bool): Flag indicating whether the record is archived.
                           Default is False.
        archived_at (datetime): Timestamp when the record was archived. Nullable.
        archive_reason (ArchiveReason): Reason for archiving the record. Nullable.
        archived_by (UUID): ID of the staff member who archived the record. Nullable.

    Methods:
        archive(archived_by, archive_reason): Marks the record as archived.
        restore(): Restores an archived record to active status.
    """

    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    archived_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    archive_reason: Mapped[ArchiveReason] = mapped_column(Enum(ArchiveReason), nullable=True)

    def archive(self, archived_by: UUID, archive_reason: ArchiveReason) -> None:
        """
        Marks the instance as archived.

        Args:
            archived_by (UUID): ID of the staff member performing the archive action.
            archive_reason (ArchiveReason): Reason why the record is being archived.
        """
        self.is_archived = True
        self.archived_at = datetime.now(timezone.utc)
        self.archived_by = archived_by
        self.archive_reason = archive_reason


    def restore(self) -> None:
        """
        Resets the is_archived flag to False and archived entity to active status.
        """
        self.is_archived = False
        self.archived_at = None
        self.archive_reason = None