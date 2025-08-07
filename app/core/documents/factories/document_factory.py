from typing import List
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.core.documents.models.documents import StudentDocument
from app.core.documents.services.document_service import DocumentService
from app.core.documents.services.validators import DocumentValidator
from app.core.shared.factory.base_factory import BaseFactory
from app.core.shared.services.lifecycle_service.archive_service import ArchiveService
from app.core.shared.services.lifecycle_service.delete_service import DeleteService
from app.infra.db.repositories.sqlalchemy_repos.base_repo import SQLAlchemyRepository
from app.core.shared.exceptions.decorators.resolve_unique_violation import resolve_unique_violation
from app.core.shared.exceptions.decorators.resolve_fk_violation import resolve_fk_on_create, resolve_fk_on_update, resolve_fk_on_delete
from app.core.shared.exceptions import EntityNotFoundError
from app.core.shared.exceptions.maps.error_map import error_map


class DocumentFactory(BaseFactory):
    """Factory class for managing Document operations."""

    def __init__(self, session: Session, model = StudentDocument, current_user = None):
        super().__init__(current_user)
        """Initialize factory.
            Args:
                session: SQLAlchemy db session
                model: Model class, defaults to Document
                current_user: The authenticated user performing the operation, if any.
        """
        self.model = model
        self.session = session
        self.current_user = current_user
        self.repository = SQLAlchemyRepository(self.model, session)
        self.validator = DocumentValidator()
        self.delete_service = DeleteService(self.model, session)
        self.archive_service = ArchiveService(session, current_user)
        self.error_details = error_map.get(self.model)
        self.entity_model, self.display_name = self.error_details
        self.actor_id: UUID = self.get_actor_id()
        self.domain = "Document"

    def raise_not_found(self, identifier, error):
        raise EntityNotFoundError(
            entity_model=self.entity_model,
            identifier=identifier,
            error=str(error),
            display_name=self.display_name
        )


    @resolve_unique_violation({
        "uq_student_document_title_student_id": ("_", "This document title exists for this student in the same academic session")
    })
    @resolve_fk_on_create()
    def create_document(self, student_id: UUID, data) -> StudentDocument:
        """Create a new Document.
        Args:
            student_id: id of document owner
            data: Document data
        Returns:
            Document: Created Document record
        """
        new_document = StudentDocument(
            id=uuid4(),
            title=self.validator.validate_name(data.title),
            student_id=student_id,
            academic_session=self.validator.validate_academic_session(data.academic_session),
            document_type = data.document_type,

            created_by=self.actor_id,
            last_modified_by=self.actor_id
        )
        return self.repository.create(new_document)


    def get_document(self, document_id: UUID) -> StudentDocument:
        """Get a specific Document by ID.
        Args:
            document_id (UUID): ID of Document to retrieve
        Returns:
            Document: Retrieved Document record
        """
        try:
            return self.repository.get_by_id(document_id)
        except EntityNotFoundError as e:
            self.raise_not_found(document_id, e)


    def get_all_documents(self, filters) -> List[StudentDocument]:
        """Get all active Documents with filtering.
        Returns:
            List[Document]: List of active Documents
        """
        fields = ['title', 'academic_session','document_type','student_id']
        return self.repository.execute_query(fields, filters)

    @resolve_unique_violation({
        "uq_student_document_title_student_id": ("_", "This document title exists for this student in the same academic session")
    })
    @resolve_fk_on_update()
    def update_document(self, document_id: UUID, data: dict) -> StudentDocument:
        """Update Document information.
        Args:
            document_id (UUID): ID of Document to update
            data (dict): Dictionary containing fields to update
        Returns:
            Document: Updated Document record
        """
        copied_data = data.copy()
        try:
            existing = self.get_document(document_id)
            validations = {
                "title": (self.validator.validate_name, "title"),
            }

            for field, (validator_func, model_attr) in validations.items():
                if field in copied_data:
                    validated_value = validator_func(copied_data.pop(field))
                    setattr(existing, model_attr, validated_value)

            for key, value in copied_data.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            return self.repository.update(document_id, existing, modified_by=self.actor_id)

        except EntityNotFoundError as e:
                self.raise_not_found(document_id, e)


    def archive_document(self, document_id: UUID, reason) -> None:
        """Archive Document
        Args:
            document_id (UUID): ID of Document to archive
            reason: Reason for archiving
        Returns:
            Document: Archived Document record
        """
        try:
            self.repository.archive(document_id, self.actor_id, reason)

        except EntityNotFoundError as e:
            self.raise_not_found(document_id, e)


    @resolve_fk_on_delete()
    def delete_document(self, document_id: UUID) -> None:
        doc_service = DocumentService(self.session, self.current_user)
        """Permanently delete an Document
        Args:
            document_id (UUID): ID of Document to delete
        """
        try:
            doc= self.get_document(document_id)

            #remove the s3 file for the document
            doc_service.remove_document_file(doc)
            self.repository.delete(document_id)

        except EntityNotFoundError as e:
            self.raise_not_found(document_id, e)


    def get_all_archived_documents(self, filters) -> List[StudentDocument]:
        """Get all archived Documents with filtering.
        Returns:
            List[Document]: List of archived Document records
        """
        fields = ['title', 'academic_session','document_type','student_id']
        return self.repository.execute_archive_query(fields, filters)


    def get_archived_document(self, document_id: UUID) -> StudentDocument:
        """Get an archived Document by ID.
        Args:
            document_id: ID of Document to retrieve
        Returns:
            Document: Retrieved Document record
        """
        try:
            return self.repository.get_archive_by_id(document_id)
        except EntityNotFoundError as e:
            self.raise_not_found(document_id, e)



    def restore_document(self, document_id: UUID) -> StudentDocument:
        """Restore an archived Document.
        Args:
            document_id: ID of Document to restore
        Returns:
            Document: Restored Document record
        """
        try:
            return self.repository.restore(document_id)
        except EntityNotFoundError as e:
            self.raise_not_found(document_id, e)


    @resolve_fk_on_delete()
    def delete_archived_document(self, document_id: UUID) -> None:
        """Permanently delete an archived Document 
        Args:
            document_id: ID of Document to delete
        """
        try:
            self.repository.delete_archive(document_id)

        except EntityNotFoundError as e:
            self.raise_not_found(document_id, e)
