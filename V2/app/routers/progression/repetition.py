from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.infra.db.session_manager import get_db
from V2.app.core.progression.crud.repetition import RepetitionCrud
from V2.app.core.progression.schemas.repetition import (
    StudentRepetitionCreate,
    StudentRepetitionResponse,
    RepetitionFilterParams
)
from V2.app.core.shared.schemas.shared_models import ArchiveRequest

router = APIRouter()


@router.post("/students/{student_id}", response_model=StudentRepetitionResponse, status_code=201)
def create_repetition(student_id: UUID, data: StudentRepetitionCreate, db: Session = Depends(get_db)):
    crud = RepetitionCrud(db)
    return crud.create_repetition(student_id, data)


@router.get("/", response_model=List[StudentRepetitionResponse])
def get_all_repetitions(filters: RepetitionFilterParams = Depends(), db: Session = Depends(get_db)):
    crud = RepetitionCrud(db)
    return crud.get_all_repetitions(filters)


@router.get("/{repetition_id}", response_model=StudentRepetitionResponse)
def get_repetition(repetition_id: UUID, db: Session = Depends(get_db)):
    crud = RepetitionCrud(db)
    return crud.get_repetition(repetition_id)


@router.put("/{repetition_id}", response_model=StudentRepetitionResponse)
def update_repetition(repetition_id: UUID, data: StudentRepetitionCreate, db: Session = Depends(get_db)):
    crud = RepetitionCrud(db)
    return crud.update_repetition(repetition_id, data)


@router.patch("/{repetition_id}", status_code=204)
def archive_repetition(repetition_id: UUID, reason: ArchiveRequest, db: Session = Depends(get_db)):
    crud = RepetitionCrud(db)
    return crud.archive_repetition(repetition_id, reason.reason)


@router.delete("/{repetition_id}", status_code=204)
def delete_repetition(repetition_id: UUID, db: Session = Depends(get_db)):
    crud = RepetitionCrud(db)
    return crud.delete_repetition(repetition_id)
