from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.core.shared.schemas.enums import ArchiveReason
from V2.app.core.documents.models.documents import StudentDocument
from V2.app.core.documents.factories.document_factory import DocumentFactory
from V2.app.core.shared.services.export_service.export import ExportService
from V2.app.core.documents.schemas.student_document import (
    DocumentFilterParams, DocumentCreate, DocumentUpdate, DocumentResponse
)


class DocumentCrud:
    """CRUD operations for documents."""

    def __init__(self, session: Session, current_user = None):
        """Initialize CRUD service.
        Args:
            session: SQLAlchemy db session
            current_user: The authenticated user performing the operation, if any.
        """
        self.session = session
        self.current_user = current_user
        self.factory = DocumentFactory(session, current_user=current_user)
        self.export_service = ExportService(session)


    def create_document(self, owner_id: UUID, data: DocumentCreate) -> DocumentResponse:
        """Create a new document"""
        new_document = self.factory.create_document(owner_id, data)
        return DocumentResponse.model_validate(new_document)


    def get_document(self, document_id: UUID) -> DocumentResponse:
        """Get document by ID."""
        document_response = self.factory.get_document(document_id)
        return DocumentResponse.model_validate(document_response)


    def get_all_documents(self, filters: DocumentFilterParams) -> List[DocumentResponse]:
        """Get all active documents."""
        documents = self.factory.get_all_documents(filters)
        return [DocumentResponse.model_validate(a_document) for a_document in documents]


    def update_document(self, document_id: UUID, data: DocumentUpdate) -> DocumentResponse:
        """Update document information."""
        data = data.model_dump(exclude_unset=True)
        updated_document = self.factory.update_document(document_id, data)
        return DocumentResponse.model_validate(updated_document)

    def archive_document(self, document_id: UUID, reason: ArchiveReason) -> None:
        """Archive a document.
        Args:
            document_id: document UUID
            reason: Reason for archiving
        Returns:
            DocumentResponse: Archived document
        """
        self.factory.archive_document(document_id, reason)

    def export_document(self, document_id: UUID, export_format: str) -> str:
        """Export document and its associated data
        Args:
            document_id: document UUID
            export_format: Preferred export format
        """
        return self.export_service.export_entity(
            StudentDocument, document_id, export_format
        )


    def delete_document(self, document_id: UUID) -> None:
        """Permanently delete a document."""
        self.factory.delete_document(document_id)


    # Archived document operations
    def get_archived_document(self, document_id: UUID) -> DocumentResponse:
        """Get an archived document by ID."""
        document_response = self.factory.get_archived_document(document_id)
        return DocumentResponse.model_validate(document_response)


    def get_all_archived_documents(self, filters: DocumentFilterParams) -> List[DocumentResponse]:
        """Get all archived documents."""
        documents = self.factory.get_all_archived_documents(filters)
        return [DocumentResponse.model_validate(a_document) for a_document in documents]


    def restore_document(self, document_id: UUID) -> DocumentResponse:
        """Restore an archived document."""
        restored_document = self.factory.restore_document(document_id)
        return DocumentResponse.model_validate(restored_document)


    def delete_archived_document(self, document_id: UUID) -> None:
        """Permanently delete an archived document."""
        self.factory.delete_archived_document(document_id)