from app.core.shared.models.common_imports import *
from app.core.shared.models.enums import Gender
from app.core.shared.models.mixins import AuditMixins, TimeStampMixins, ArchiveMixins


class UserBase(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """Abstract base class for users"""

    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )
    current_role_id: Mapped[UUID] = mapped_column(
        ForeignKey("roles.id", ondelete="RESTRICT"), nullable=True
    )  # temp
    password_hash: Mapped[str] = mapped_column(String(300))
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    gender: Mapped[Gender] = mapped_column(Enum(Gender, name="gender"))
    profile_s3_key: Mapped[str] = mapped_column(String(200), nullable=True)

    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    exported: Mapped[bool] = mapped_column(Boolean, default=False)
    deletion_eligible: Mapped[bool] = mapped_column(Boolean, default=False)
