
from typing import List
from uuid import UUID
from fastapi import Depends, APIRouter

from V2.app.core.documents.crud.documents import DocumentCrud
from V2.app.core.documents.schemas.student_document import DocumentFilterParams, DocumentResponse
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[DocumentResponse])
def get_archived_documents(
        filters: DocumentFilterParams = Depends(),
        crud: DocumentCrud = Depends(get_authenticated_crud(DocumentCrud))
    ):
    return crud.get_all_archived_documents(filters)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_archived_document(
        document_id: UUID,
        crud: DocumentCrud = Depends(get_authenticated_crud(DocumentCrud))
    ):
    return crud.get_archived_document(document_id)


@router.patch("/{document_id}", response_model=DocumentResponse)
def restore_document(
        document_id: UUID,
        crud: DocumentCrud = Depends(get_authenticated_crud(DocumentCrud))
    ):
    return crud.restore_document(document_id)


@router.delete("/{document_id}", status_code=204)
def delete_archived_document(
        document_id: UUID,
        crud: DocumentCrud = Depends(get_authenticated_crud(DocumentCrud))
    ):
    return crud.delete_archived_document(document_id)




