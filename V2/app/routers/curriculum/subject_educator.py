from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.curriculum.crud.subject_educator import SubjectEducatorCrud
from V2.app.core.curriculum.schemas.subject_educator import(
    SubjectEducatorCreate, SubjectEducatorFilterParams, SubjectEducatorResponse
)


router = APIRouter()

@router.post("/", response_model= SubjectEducatorResponse, status_code=201)
def assign_subject_educator(data:SubjectEducatorCreate,db: Session = Depends(get_db)):
    subject_educator_crud = SubjectEducatorCrud(db)
    return subject_educator_crud.create_subject_educator(data)


@router.get("/", response_model=List[SubjectEducatorResponse])
def get_subject_educators(filters: SubjectEducatorFilterParams = Depends(),db: Session = Depends(get_db)):
    subject_educator_crud = SubjectEducatorCrud(db)
    return subject_educator_crud.get_all_subject_educators(filters)


@router.get("/{subject_educator_id}", response_model=SubjectEducatorResponse)
def get_subject_educator(subject_educator_id: UUID, db: Session = Depends(get_db)):
    subject_educator_crud = SubjectEducatorCrud(db)
    return subject_educator_crud.get_subject_educator(subject_educator_id)



@router.patch("/{subject_educator_id}",  status_code=204)
def archive_subject_educator(subject_educator_id: UUID, reason:ArchiveRequest,
                       db: Session = Depends(get_db)):
    subject_educator_crud = SubjectEducatorCrud(db)
    return subject_educator_crud.archive_subject_educator(subject_educator_id, reason.reason)


@router.post("/{subject_educator_id}", response_class=FileResponse,  status_code=204)
def export_subject_educator(subject_educator_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    subject_educator_crud = SubjectEducatorCrud(db)
    file_path= subject_educator_crud.export_subject_educator(subject_educator_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{subject_educator_id}", status_code=204)
def delete_subject_educator(subject_educator_id: UUID, db: Session = Depends(get_db)):
    subject_educator_crud = SubjectEducatorCrud(db)
    return subject_educator_crud.delete_subject_educator(subject_educator_id)










