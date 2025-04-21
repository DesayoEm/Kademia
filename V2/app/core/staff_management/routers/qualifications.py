from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import Query
from typing import Annotated
from fastapi.responses import FileResponse

from fastapi import Depends, APIRouter
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.database.session_manager import get_db
from V2.app.core.staff_management.crud.educator_qualification import QualificationCrud
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from V2.app.core.staff_management.schemas.educator_qualification import(
    QualificationCreate, QualificationUpdate, QualificationResponse, QualificationFilterParams
)


router = APIRouter()

@router.post("/", response_model= QualificationResponse, status_code=201)
def create_qualification(data:QualificationCreate,
                db: Session = Depends(get_db)):
        qualifications_crud = QualificationCrud(db)
        return qualifications_crud.create_qualification(data)


@router.get("/", response_model=list[QualificationResponse])
def get_qualifications(filters: Annotated[QualificationFilterParams, Query()],
                db: Session = Depends(get_db)):
        qualifications_crud = QualificationCrud(db)
        return qualifications_crud.get_all_qualifications(filters)


@router.get("/{qualification_id}", response_model=QualificationResponse)
def get_qualification(qualification_id: UUID, db: Session = Depends(get_db)):
        qualifications_crud = QualificationCrud(db)
        return qualifications_crud.get_qualification(qualification_id)


@router.put("/{qualification_id}", response_model=QualificationResponse)
def update_qualification(data: QualificationUpdate, qualification_id: UUID,
                         db: Session = Depends(get_db)):
        qualifications_crud = QualificationCrud(db)
        return qualifications_crud.update_qualification(qualification_id, data)


@router.patch("/{qualification_id}", status_code=204)
def archive_qualification(qualification_id: UUID, reason:ArchiveRequest,
                          db: Session = Depends(get_db)):
        qualifications_crud = QualificationCrud(db)
        return qualifications_crud.archive_qualification(qualification_id, reason.reason)


@router.post("/{qualification_id}", response_class=FileResponse,  status_code=204)
def export_qualification(qualification_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    qualifications_crud = QualificationCrud(db)
    file_path= qualifications_crud.export_qualification(qualification_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{qualification_id}", status_code=204)
def delete_qualification(qualification_id: UUID, db: Session = Depends(get_db)):
        qualifications_crud = QualificationCrud(db)
        return qualifications_crud.delete_qualification(qualification_id)











