from sqlalchemy.orm import Session
from uuid import UUID
from V2.app.core.identity.schemas.staff import StaffResponse, StaffFilterParams
from fastapi import Depends, APIRouter
from V2.app.core.shared.database.session_manager import get_db
from V2.app.core.identity.crud.staff import StaffCrud
from fastapi import Query
from typing import Annotated

router = APIRouter()

@router.get("/", response_model=list[StaffResponse])
def get_archived_staff(filters: Annotated[StaffFilterParams, Query()],
        db: Session = Depends(get_db)):
    staff_crud = StaffCrud(db)
    return staff_crud.get_all_archived_staff(filters)


@router.get("/{staff_id}", response_model=StaffResponse)
def get_archived_staff(staff_id: UUID, db: Session = Depends(get_db)):
    staff_crud = StaffCrud(db)
    return staff_crud.get_archived_staff(staff_id)


@router.patch("/{staff_id}", response_model=StaffResponse)
def restore_staff(staff_id: UUID, db: Session = Depends(get_db)):
    staff_crud = StaffCrud(db)
    return staff_crud.restore_staff(staff_id)


@router.delete("/{staff_id}", status_code=204)
def delete_archived_staff(staff_id: UUID, db: Session = Depends(get_db)):
    staff_crud = StaffCrud(db)
    return staff_crud.delete_archived_staff(staff_id)











