
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse
from fastapi import UploadFile, File

from app.core.identity.factories.student import StudentFactory
from app.core.shared.schemas.enums import ExportFormat
from app.core.shared.schemas.shared_models import ArchiveRequest, UploadResponse
from fastapi import Depends, APIRouter
from app.core.documents.factories.document_factory import DocumentFactory
from app.core.documents.services.document_service import DocumentService
from app.core.documents.schemas.student_document import (
    DocumentFilterParams, DocumentCreate, DocumentUpdate, DocumentResponse, DocumentAudit
)
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service

from app.core.shared.services.file_storage.s3_upload import S3Upload


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("/{student_id}/documents/{document_id}/file", response_model= UploadResponse,
             status_code=201)
def upload_document_file(
        doc_id: UUID,
        student_id: UUID,
        file: UploadFile = File(...),
        service: DocumentService = Depends(get_authenticated_service(DocumentService)),
        doc_factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory)),
        student_factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
        document = doc_factory.get_document(doc_id)
        student = student_factory.get_student(student_id)
        result = service.upload_document_file(file, student, document)

        return UploadResponse(**result)



@router.get("/{document_id}/file")
def get_document_file(
        document_id: UUID,
        service: S3Upload = Depends(get_authenticated_service(S3Upload)),
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
        document = factory.get_document(document_id)
        key = document.document_s3_key
        return service.generate_presigned_url(key)


@router.delete("/{document_id}/file", status_code=204)
def remove_document_file(
        document_id: UUID,
        service: DocumentService = Depends(get_authenticated_service(DocumentService)),
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
        document = factory.get_document(document_id)
        return service.remove_document_file(document)


@router.post("{student_id}/", response_model= DocumentResponse, status_code=201)
def create_document(
        student_id: UUID,
        payload:DocumentCreate,
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
    return factory.create_document(student_id, payload)


@router.get("/", response_model=List[DocumentResponse])
def get_documents(
        filters: DocumentFilterParams = Depends(),
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
    return factory.get_all_documents(filters)


@router.get("/{document_id}/audit", response_model=DocumentAudit)
def get_document_audit(
        document_id: UUID,
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
    return factory.get_document(document_id)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
        document_id: UUID,
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
    return factory.get_document(document_id)


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
        payload: DocumentUpdate,
        document_id: UUID,
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
    payload = payload.model_dump(exclude_unset=True)
    return factory.update_document(document_id, payload)


@router.patch("/{document_id}",  status_code=204)
def archive_document(
        document_id: UUID,
        reason:ArchiveRequest,
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
    return factory.archive_document(document_id, reason.reason)


@router.post("/{document_id}/audit", response_class=FileResponse,  status_code=204)
def export_document_audit(
        document_id: UUID,
        export_format: ExportFormat,
        service: DocumentService = Depends(get_authenticated_service(DocumentService))
    ):
    file_path= service.export_document_audit(document_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{document_id}", status_code=204)
def delete_document(
        document_id: UUID,
        factory: DocumentFactory = Depends(get_authenticated_factory(DocumentFactory))
    ):
    return factory.delete_document(document_id)










