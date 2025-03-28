from sqlalchemy.orm import Session
from uuid import UUID

from ....schemas.users.staff import StaffCreate, StaffUpdate, StaffResponse, StaffFilterParams
from fastapi import Depends, APIRouter
from ....database.session import get_db
from ....crud.users.staff import StaffCrud
from ....schemas.shared_models import ArchiveRequest
from ....core.services.auth.dependencies import TokenBearer
from fastapi import Query
from typing import Annotated

router = APIRouter()
bearer= TokenBearer()

@router.post("/", response_model= StaffResponse, status_code=201)
def create_staff(data:StaffCreate,db: Session = Depends(get_db),
                        ):
        staff_crud = StaffCrud(db)
        return staff_crud.create_staff(data)


@router.get("/", response_model=list[StaffResponse])
def get_staff(filters: Annotated[StaffFilterParams, Query()],
                db: Session = Depends(get_db)):
        staff_crud = StaffCrud(db)
        return staff_crud.get_all_staff(filters)


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: UUID, db: Session = Depends(get_db)):
        staff_crud = StaffCrud(db)
        return staff_crud.get_staff(staff_id)


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(data: StaffUpdate, staff_id: UUID,
                         db: Session = Depends(get_db)):
        staff_crud = StaffCrud(db)
        return staff_crud.update_staff(staff_id, data)


@router.patch("/{staff_id}", status_code=204)
def archive_staff(staff_id: UUID, reason:ArchiveRequest,
                          db: Session = Depends(get_db)):
        staff_crud = StaffCrud(db)
        return staff_crud.archive_staff(staff_id, reason.reason)


@router.delete("/{staff_id}", status_code=204)
def delete_staff(staff_id: UUID, db: Session = Depends(get_db)):
        staff_crud = StaffCrud(db)
        return staff_crud.delete_staff(staff_id)











