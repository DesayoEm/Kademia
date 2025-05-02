from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.documents.crud.awards import AwardCrud
from V2.app.core.documents.schemas.student_award import(
    AwardFilterParams, AwardCreate, AwardUpdate, AwardResponse
)


router = APIRouter()

@router.post("/", response_model= AwardResponse, status_code=201)
def create_award(data:AwardCreate,db: Session = Depends(get_db)):
    award_crud = AwardCrud(db)
    return award_crud.create_award(data)


@router.get("/", response_model=List[AwardResponse])
def get_awards(filters: AwardFilterParams = Depends(),db: Session = Depends(get_db)):
    award_crud = AwardCrud(db)
    return award_crud.get_all_awards(filters)


@router.get("/{award_id}", response_model=AwardResponse)
def get_award(award_id: UUID, db: Session = Depends(get_db)):
    award_crud = AwardCrud(db)
    return award_crud.get_award(award_id)


@router.put("/{award_id}", response_model=AwardResponse)
def update_award(data: AwardUpdate, award_id: UUID,db: Session = Depends(get_db)):
    award_crud = AwardCrud(db)
    return award_crud.update_award(award_id, data)


@router.patch("/{award_id}",  status_code=204)
def archive_award(award_id: UUID, reason:ArchiveRequest,
                       db: Session = Depends(get_db)):
    award_crud = AwardCrud(db)
    return award_crud.archive_award(award_id, reason.reason)


@router.post("/{award_id}", response_class=FileResponse,  status_code=204)
def export_award(award_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    award_crud = AwardCrud(db)
    file_path= award_crud.export_award(award_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{award_id}", status_code=204)
def delete_award(award_id: UUID, db: Session = Depends(get_db)):
    award_crud = AwardCrud(db)
    return award_crud.delete_award(award_id)










