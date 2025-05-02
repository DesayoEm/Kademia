from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.documents.crud.documents import DocumentCrud
from V2.app.core.documents.schemas.student_document import DocumentFilterParams, DocumentResponse


router = APIRouter()


@router.get("/", response_model=List[DocumentResponse])
def get_archived_documents(filters: DocumentFilterParams = Depends(),db: Session = Depends(get_db)):
    document_crud = DocumentCrud(db)
    return document_crud.get_all_archived_documents(filters)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_archived_document(document_id: UUID, db: Session = Depends(get_db)):
    document_crud = DocumentCrud(db)
    return document_crud.get_archived_document(document_id)


@router.patch("/{document_id}", response_model=DocumentResponse)
def restore_document(document_id: UUID,db: Session = Depends(get_db)):
    document_crud = DocumentCrud(db)
    return document_crud.restore_document(document_id)


@router.delete("/{document_id}", status_code=204)
def delete_archived_document(document_id: UUID, db: Session = Depends(get_db)):
    document_crud = DocumentCrud(db)
    return document_crud.delete_archived_document(document_id)




