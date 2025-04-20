from sqlalchemy.orm import Session
from uuid import UUID
from V2.app.core.staff_management.schemas.educator_qualification import(
    QualificationCreate, QualificationUpdate, QualificationResponse, QualificationFilterParams
)
from fastapi import Depends, APIRouter
from V2.app.core.shared.database import get_db
from V2.app.core.staff_management.crud.educator_qualification import QualificationCrud
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Query
from typing import Annotated

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


@router.delete("/{qualification_id}", status_code=204)
def delete_qualification(qualification_id: UUID, db: Session = Depends(get_db)):
        qualifications_crud = QualificationCrud(db)
        return qualifications_crud.delete_qualification(qualification_id)











