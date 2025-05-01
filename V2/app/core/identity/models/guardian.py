from .base import UserBase

from V2.app.core.shared.models.common_imports import *
from V2.app.core.shared.models.enums import AccessLevel, Title, UserType

class Guardian(UserBase):
    """
    Represents a parent or guardian of students, including contact information and relationship with the students they oversee.
    Inherits from ProfileBase.
    """
    __tablename__ = 'guardians'

    title: Mapped[Title] = mapped_column(Enum(Title, name='title'))
    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel, name='accesslevel'), default=AccessLevel.READ)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType, name='usertype'), default=UserType.GUARDIAN)
    image_url: Mapped[str] = mapped_column(String(225), nullable=True)
    email_address: Mapped[str] = mapped_column(String(255), unique=True)
    address: Mapped[str] = mapped_column(String(500))
    phone: Mapped[str] = mapped_column(String(14), unique=True)

    # Relationships
    wards: Mapped[List['Student']] = relationship(back_populates='guardian')

    __table_args__ = (
        Index('idx_guardians_name', 'first_name', 'last_name'),
        Index('idx_guardians_email', 'email_address'),
        Index('idx_guardians_phone', 'phone'),
        Index('idx_guardian_archived_at', 'archived_at'),
    )

    def __repr__(self) -> str:
        return f"Parent(name={self.first_name} {self.last_name}, phone={self.phone})"

