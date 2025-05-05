from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.infra.db.session_manager import get_db
from V2.app.core.transfer.crud.department_transfer import StudentDepartmentTransferCrud
from V2.app.core.transfer.schemas.department_transfer import (
    StudentDepartmentTransferCreate,
    StudentDepartmentTransferUpdate,
    StudentDepartmentTransferResponse,
    DepartmentTransferFilterParams
)
from V2.app.core.shared.schemas.shared_models import ArchiveRequest

router = APIRouter()


@router.post("/students/{student_id}", response_model=StudentDepartmentTransferResponse, status_code=201)
def create_transfer(student_id: UUID, data: StudentDepartmentTransferCreate, db: Session = Depends(get_db)):
    crud = StudentDepartmentTransferCrud(db)
    return crud.create_transfer(student_id, data)


@router.get("/", response_model=List[StudentDepartmentTransferResponse])
def get_transfers(filters: DepartmentTransferFilterParams = Depends(), db: Session = Depends(get_db)):
    crud = StudentDepartmentTransferCrud(db)
    return crud.get_all_transfers(filters)


@router.get("/{transfer_id}", response_model=StudentDepartmentTransferResponse)
def get_transfer(transfer_id: UUID, db: Session = Depends(get_db)):
    crud = StudentDepartmentTransferCrud(db)
    return crud.get_transfer(transfer_id)


@router.put("/{transfer_id}", response_model=StudentDepartmentTransferResponse)
def update_transfer(transfer_id: UUID, data: StudentDepartmentTransferUpdate, db: Session = Depends(get_db)):
    crud = StudentDepartmentTransferCrud(db)
    return crud.update_transfer(transfer_id, data)


@router.patch("/{transfer_id}", status_code=204)
def archive_transfer(transfer_id: UUID, reason: ArchiveRequest, db: Session = Depends(get_db)):
    crud = StudentDepartmentTransferCrud(db)
    return crud.archive_transfer(transfer_id, reason.reason)


@router.delete("/{transfer_id}", status_code=204)
def delete_transfer(transfer_id: UUID, db: Session = Depends(get_db)):
    crud = StudentDepartmentTransferCrud(db)
    return crud.delete_transfer(transfer_id)
