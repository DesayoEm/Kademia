from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.infra.db.session_manager import get_db
from V2.app.core.transfer.crud.class_transfer import ClassTransferCrud
from V2.app.core.transfer.schemas.class_transfer import (
    StudentClassTransferResponse,
    ClassTransferFilterParams
)

router = APIRouter()


@router.get("/", response_model=List[StudentClassTransferResponse])
def get_archived_transfers(filters: ClassTransferFilterParams = Depends(), db: Session = Depends(get_db)):
    crud = ClassTransferCrud(db)
    return crud.get_all_archived_transfers(filters)


@router.get("/{transfer_id}", response_model=StudentClassTransferResponse)
def get_archived_transfer(transfer_id: UUID, db: Session = Depends(get_db)):
    crud = ClassTransferCrud(db)
    return crud.get_archived_transfer(transfer_id)


@router.patch("/{transfer_id}", response_model=StudentClassTransferResponse)
def restore_transfer(transfer_id: UUID, db: Session = Depends(get_db)):
    crud = ClassTransferCrud(db)
    return crud.restore_transfer(transfer_id)


@router.delete("/{transfer_id}", status_code=204)
def delete_archived_transfer(transfer_id: UUID, db: Session = Depends(get_db)):
    crud = ClassTransferCrud(db)
    return crud.delete_archived_transfer(transfer_id)
