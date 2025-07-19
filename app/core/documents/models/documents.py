from app.core.shared.models.common_imports import *
from app.core.shared.models.mixins import AuditMixins, TimeStampMixins, ArchiveMixins
from app.core.shared.models.enums import DocumentType


class StudentDocument(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """Manages documents uploaded for students.
    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'student_documents'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
            ondelete='RESTRICT',name='fk_student_documents_students_owner_id'),default=uuid4
        )
    title: Mapped[str] = mapped_column(String(50))
    academic_session: Mapped[str] = mapped_column(String(9))
    document_type: Mapped[DocumentType] = mapped_column(Enum(DocumentType, name='documenttype'))
    document_s3_key: Mapped[str] = mapped_column(String(225), nullable = True)

    # Relationships
    owner: Mapped['Student'] = relationship(back_populates='documents_owned', foreign_keys='[StudentDocument.owner_id]')

    __table_args__ = (
        UniqueConstraint('owner_id', 'title', name = "uq_student_document_title_owner_id"),
        Index('idx_owner_document_type', 'owner_id', 'document_type'),
        Index('idx_academic_session', 'academic_session'),
    )

    def __repr__(self) -> str:
        return f"Document(name={self.document_type}, {self.title}, owner={self.owner_id})"


class StudentAward(Base, AuditMixins, TimeStampMixins, ArchiveMixins):
    """
    Represents an award earned by a student
    Inherits from Base, AuditMixins, TimeStampMixins, and ArchiveMixins.
    """
    __tablename__ = 'student_awards'
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey('students.id',
         ondelete='CASCADE',name='fk_student_documents_students_owner_id')
        )
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(225), nullable = True)
    academic_session: Mapped[str] = mapped_column(String(9))
    award_s3_key: Mapped[str] = mapped_column(String(225), nullable = True)

    # Relationships
    owner: Mapped['Student'] = relationship(back_populates='awards_earned',
            foreign_keys='[StudentAward.owner_id]', passive_deletes=True)

    __table_args__ = (
        UniqueConstraint('owner_id', 'title', name="uq_student_award_title_owner_id"),
        Index('idx_owner_title', 'owner_id', 'title'),
    )

    def __repr__(self) -> str:
        return f"Document(name={self.title}, owner={self.owner_id})"


from app.core.identity.models.student import Student