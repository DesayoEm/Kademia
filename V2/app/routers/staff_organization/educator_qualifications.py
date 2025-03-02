from sqlalchemy.orm import Session
from uuid import UUID

from ...database.models.data_enums import ArchiveReason
from ...schemas.staff_organization.educator_qualifications import(
    QualificationCreate, QualificationUpdate, QualificationResponse, QualificationFilterParams
)
from fastapi import Depends, APIRouter
from ...database.session_manager import get_db
from ...crud.staff_organization.educator_qualifications import QualificationsCrud
from fastapi import Query
from typing import Annotated

router = APIRouter()


@router.post("/", response_model= QualificationResponse, status_code=201)
def create_qualification(
        data:QualificationCreate,
        db: Session = Depends(get_db)):
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.create_qualification(data)


@router.get("/", response_model=list[QualificationResponse])
def get_qualifications(
        filters: Annotated[QualificationFilterParams, Query()],
        db: Session = Depends(get_db)):
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.get_all_qualifications(filters)


@router.get("/{qualification_id}", response_model=QualificationResponse)
def get_qualification(qualification_id: UUID, db: Session = Depends(get_db)):
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.get_qualification(qualification_id)


@router.put("/{qualification_id}", response_model=QualificationResponse)
def update_qualification(data: QualificationUpdate, qualification_id: UUID,
                         db: Session = Depends(get_db)):
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.update_qualification(qualification_id, data)


@router.patch("/{qualification_id}", response_model=QualificationResponse)
def archive_qualification(qualification_id: UUID, reason:ArchiveReason,
                          db: Session = Depends(get_db)):
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.archive_qualification(qualification_id, reason)


@router.delete("/{qualification_id}", status_code=204)
def delete_qualification(qualification_id: UUID, db: Session = Depends(get_db)):
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.delete_qualification(qualification_id)











