from sqlalchemy.orm import Session
from uuid import UUID

from ...database.models.data_enums import ArchiveReason
from ...schemas.staff_organization.educator_qualifications import(
    QualificationCreate, QualificationUpdate, QualificationResponse, QualificationFilterParams
)
from fastapi import Depends, APIRouter
from ...database.session_manager import get_db
from ...crud.staff_organization.educator_qualifications import QualificationsCrud
from fastapi import HTTPException, Query
from typing import Annotated

from ...services.errors.database_errors import (
    EntityNotFoundError, DatabaseError,
)
router = APIRouter()


@router.post("/", response_model= QualificationResponse, status_code=201)
def create_qualification(
        data:QualificationCreate,
        db: Session = Depends(get_db)):
    try:
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.create_qualification(data)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=list[QualificationResponse])
def get_qualifications(
        filters: Annotated[QualificationFilterParams, Query()],
        db: Session = Depends(get_db)):
    try:
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.get_all_qualifications(filters)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{qualification_id}", response_model=QualificationResponse)
def get_qualification(qualification_id: UUID, db: Session = Depends(get_db)):
    try:
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.get_qualification(qualification_id)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{qualification_id}", response_model=QualificationResponse)
def update_qualification(data: QualificationUpdate, qualification_id: UUID,
                         db: Session = Depends(get_db)):
    try:
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.update_qualification(qualification_id, data)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{qualification_id}", response_model=QualificationResponse)
def archive_qualification(qualification_id: UUID, reason:ArchiveReason,
                          db: Session = Depends(get_db)):
    try:
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.archive_qualification(qualification_id, reason)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{qualification_id}", status_code=204)
def delete_qualification(qualification_id: UUID, db: Session = Depends(get_db)):
    try:
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.delete_qualification(qualification_id)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))











