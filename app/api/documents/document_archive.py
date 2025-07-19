
from typing import List
from uuid import UUID
from fastapi import Depends, APIRouter

from app.core.documents.factories.document_factory import DocumentFactory
from app.core.documents.schemas.student_document import DocumentFilterParams, DocumentResponse, DocumentAudit
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[DocumentResponse])
def get_archived_documents(
        filters: DocumentFilterParams = Depends(),
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
    return factory.get_all_archived_documents(filters)


@router.get("/{document_id}/audit", response_model=DocumentAudit)
def get_archived_document_audit(
        document_id: UUID,
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
    return factory.get_archived_document(document_id)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_archived_document(
        document_id: UUID,
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
    return factory.get_archived_document(document_id)


@router.patch("/{document_id}", response_model=DocumentResponse)
def restore_document(
        document_id: UUID,
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
    return factory.restore_document(document_id)



@router.delete("/{document_id}", status_code=204)
def delete_archived_document(
        document_id: UUID,
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
    return factory.delete_archived_document(document_id)




