from base import *
from validators import DocumentType


class StudentDocuments(Base):
    __tablename__ = 'student_documents'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey('students.id'), nullable=False)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    academic_year: Mapped[int] = mapped_column(Integer, nullable=False)
    document_type: Mapped[DocumentType] = mapped_column(Enum(DocumentType), nullable=False)
    file_path: Mapped[str] = mapped_column(String(225), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), nullable=False)
    uploaded_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default = func.now(), onupdate=func.now(), nullable=False)
    updated_by: Mapped[UUID] = mapped_column(ForeignKey('staff.id'), nullable=False)

    #Relationships
    owner = relationship('Students', back_populates='documents')
    uploader = relationship('Staff', foreign_keys = [uploaded_by])
    updater = relationship('Staff', foreign_keys = [updated_by])

    def __repr__(self) -> str:
        return f"Document(name={self.document_type},  {self.title}, owner={self.owner_id})"





# status varchar
# upload_date timestamp
# verified_at timestamp
# verified_by uuid [ref: > educators.id]
# }
