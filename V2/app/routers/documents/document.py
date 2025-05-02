from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.documents.crud.documents import DocumentCrud
from V2.app.core.documents.schemas.student_document import(
    DocumentFilterParams, DocumentCreate, DocumentUpdate, DocumentResponse
)


router = APIRouter()

@router.post("/", response_model= DocumentResponse, status_code=201)
def create_document(data:DocumentCreate,db: Session = Depends(get_db)):
    document_crud= DocumentCrud(db)
    return document_crud.create_document(data)


@router.get("/", response_model=List[DocumentResponse])
def get_documents(filters: DocumentFilterParams = Depends(),db: Session = Depends(get_db)):
    document_crud= DocumentCrud(db)
    return document_crud.get_all_documents(filters)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: UUID, db: Session = Depends(get_db)):
    document_crud= DocumentCrud(db)
    return document_crud.get_document(document_id)


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(data: DocumentUpdate, document_id: UUID,db: Session = Depends(get_db)):
    document_crud= DocumentCrud(db)
    return document_crud.update_document(document_id, data)


@router.patch("/{document_id}",  status_code=204)
def archive_document(document_id: UUID, reason:ArchiveRequest,
                       db: Session = Depends(get_db)):
    document_crud= DocumentCrud(db)
    return document_crud.archive_document(document_id, reason.reason)


@router.post("/{document_id}", response_class=FileResponse,  status_code=204)
def export_document(document_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    document_crud= DocumentCrud(db)
    file_path= document_crud.export_document(document_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{document_id}", status_code=204)
def delete_document(document_id: UUID, db: Session = Depends(get_db)):
    document_crud= DocumentCrud(db)
    return document_crud.delete_document(document_id)










