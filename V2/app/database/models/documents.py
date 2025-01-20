from V2.app.database.models.common_imports import *
from V2.app.database.models.data_enums import DocumentType
from V2.app.database.models.mixins import AuditMixins, SoftDeleteMixins, TimeStampMixins
import uuid


class StudentDocuments(Base, AuditMixins, TimeStampMixins, SoftDeleteMixins):
    """Manages documents uploaded for students.
    Maintains audit history with staff references defaulting to placeholder text
    (e.g., 'Anon User (left)') when referenced staff is deleted.

    Inherits from Base, AuditMixins, TimeStampMixins, and SoftDeleteMixins.
    """
    __tablename__ = 'student_documents'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    owner_id: Mapped[UUID] =mapped_column(UUID(as_uuid=True), default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(50))
    academic_year: Mapped[int] = mapped_column(Integer)
    document_type: Mapped[DocumentType] = mapped_column(Enum(DocumentType))
    file_path: Mapped[str] = mapped_column(String(225))


    __table_args__ = (
        Index('idx_owner_document_type', 'owner_id', 'document_type'),
        Index('idx_academic_year', 'academic_year'),
    )

    def __repr__(self) -> str:
        return f"Document(name={self.document_type}, {self.title}, owner={self.owner_id})"