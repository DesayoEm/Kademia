from sqlalchemy.orm import Session
from uuid import UUID
from ...schemas.staff_organization.educator_qualification import QualificationResponse, QualificationFilterParams
from fastapi import Depends, APIRouter
from ...database.session import get_db
from ...crud.staff_organization.educator_qualification import QualificationCrud
from fastapi import Query
from typing import Annotated

router = APIRouter()

@router.get("/", response_model=list[QualificationResponse])
def get_archived_qualifications(filters: Annotated[QualificationFilterParams, Query()],
        db: Session = Depends(get_db)):
    qualifications_crud = QualificationCrud(db)
    return qualifications_crud.get_all_archived_qualifications(filters)


@router.get("/{qualification_id}", response_model=QualificationResponse)
def get_archived_qualification(qualification_id: UUID, db: Session = Depends(get_db)):
    qualifications_crud = QualificationCrud(db)
    return qualifications_crud.get_archived_qualification(qualification_id)


@router.patch("/{qualification_id}", response_model=QualificationResponse)
def restore_qualification(qualification_id: UUID, db: Session = Depends(get_db)):
    qualifications_crud = QualificationCrud(db)
    return qualifications_crud.restore_qualification(qualification_id)


@router.delete("/{qualification_id}", status_code=204)
def delete_archived_qualification(qualification_id: UUID, db: Session = Depends(get_db)):
    qualifications_crud = QualificationCrud(db)
    return qualifications_crud.delete_archived_qualification(qualification_id)











