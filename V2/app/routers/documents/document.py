
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter

from V2.app.core.documents.crud.documents import DocumentCrud
from V2.app.core.documents.schemas.student_document import(
    DocumentFilterParams, DocumentCreate, DocumentUpdate, DocumentResponse
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("{student_id}/", response_model= DocumentResponse, status_code=201)
def create_document(
        student_id: UUID,
        data:DocumentCreate,
        crud: DocumentCrud = Depends(get_authenticated_crud(DocumentCrud))
    ):
    return crud.create_document(student_id, data)


@router.get("/", response_model=List[DocumentResponse])
def get_documents(
        filters: DocumentFilterParams = Depends(),
        crud: DocumentCrud = Depends(get_authenticated_crud(DocumentCrud))
    ):
    return crud.get_all_documents(filters)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
        document_id: UUID,
        crud: DocumentCrud = Depends(get_authenticated_crud(DocumentCrud))
    ):
    return crud.get_document(document_id)


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
        data: DocumentUpdate,
        document_id: UUID,
        crud: DocumentCrud = Depends(get_authenticated_crud(DocumentCrud))
    ):
    return crud.update_document(document_id, data)


@router.patch("/{document_id}",  status_code=204)
def archive_document(
        document_id: UUID,
        reason:ArchiveRequest,
        crud: DocumentCrud = Depends(get_authenticated_crud(DocumentCrud))
    ):
    return crud.archive_document(document_id, reason.reason)


@router.post("/{document_id}", response_class=FileResponse,  status_code=204)
def export_document(
        document_id: UUID,
        export_format: ExportFormat,
        crud: DocumentCrud = Depends(get_authenticated_crud(DocumentCrud))
    ):
    file_path= crud.export_document(document_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{document_id}", status_code=204)
def delete_document(
        document_id: UUID,
        crud: DocumentCrud = Depends(get_authenticated_crud(DocumentCrud))
    ):
    return crud.delete_document(document_id)










