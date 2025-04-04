from .common_imports import *
from .enums import DocumentType
from .mixins import AuditMixins, ArchiveMixins, TimeStampMixins


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
    academic_year: Mapped[int] = mapped_column(Integer)
    document_type: Mapped[DocumentType] = mapped_column(Enum(DocumentType, name='documenttype'))
    file_url: Mapped[str] = mapped_column(String(225))

    # Relationships
    owner: Mapped['Student'] = relationship(back_populates='documents_owned', foreign_keys='[StudentDocument.owner_id]')

    __table_args__ = (
        Index('idx_owner_document_type', 'owner_id', 'document_type'),
        Index('idx_academic_year', 'academic_year'),
    )

    def __repr__(self) -> str:
        return f"Document(name={self.document_type}, {self.title}, owner={self.owner_id})"