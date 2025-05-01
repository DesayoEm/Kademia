from sqlalchemy.orm import Session
from uuid import UUID

from V2.app.infra.db.session_manager import get_db
from V2.app.core.staff_management.crud.educator_qualification import QualificationCrud
from V2.app.core.staff_management.schemas.educator_qualification import QualificationResponse, QualificationFilterParams
from fastapi import Depends, APIRouter


router = APIRouter()

@router.get("/", response_model=list[QualificationResponse])
def get_archived_qualifications(filters: QualificationFilterParams = Depends(),db: Session = Depends(get_db)):
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











