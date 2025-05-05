from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.infra.db.session_manager import get_db
from V2.app.core.transfer.crud.department_transfer import StudentDepartmentTransferCrud
from V2.app.core.transfer.schemas.department_transfer import (
    StudentDepartmentTransferResponse,
    DepartmentTransferFilterParams
)

router = APIRouter()


@router.get("/", response_model=List[StudentDepartmentTransferResponse])
def get_archived_transfers(filters: DepartmentTransferFilterParams = Depends(), db: Session = Depends(get_db)):
    crud = StudentDepartmentTransferCrud(db)
    return crud.get_all_archived_transfers(filters)


@router.get("/{transfer_id}", response_model=StudentDepartmentTransferResponse)
def get_archived_transfer(transfer_id: UUID, db: Session = Depends(get_db)):
    crud = StudentDepartmentTransferCrud(db)
    return crud.get_archived_transfer(transfer_id)


@router.patch("/{transfer_id}", response_model=StudentDepartmentTransferResponse)
def restore_transfer(transfer_id: UUID, db: Session = Depends(get_db)):
    crud = StudentDepartmentTransferCrud(db)
    return crud.restore_transfer(transfer_id)


@router.delete("/{transfer_id}", status_code=204)
def delete_archived_transfer(transfer_id: UUID, db: Session = Depends(get_db)):
    crud = StudentDepartmentTransferCrud(db)
    return crud.delete_archived_transfer(transfer_id)
