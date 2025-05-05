from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.infra.db.session_manager import get_db
from V2.app.core.progression.crud.graduation import GraduationCrud
from V2.app.core.progression.schemas.graduation import (
    GraduationCreate,
    GraduationResponse,
    GraduationFilterParams
)
from V2.app.core.shared.schemas.shared_models import ArchiveRequest

router = APIRouter()


@router.post("/students/{student_id}", response_model=GraduationResponse, status_code=201)
def create_graduation(student_id: UUID, data: GraduationCreate, db: Session = Depends(get_db)):
    crud = GraduationCrud(db)
    return crud.create_graduation(student_id, data)


@router.get("/", response_model=List[GraduationResponse])
def get_all_graduations(filters: GraduationFilterParams = Depends(), db: Session = Depends(get_db)):
    crud = GraduationCrud(db)
    return crud.get_all_graduations(filters)


@router.get("/{graduation_id}", response_model=GraduationResponse)
def get_graduation(graduation_id: UUID, db: Session = Depends(get_db)):
    crud = GraduationCrud(db)
    return crud.get_graduation(graduation_id)


@router.put("/{graduation_id}", response_model=GraduationResponse)
def update_graduation(graduation_id: UUID, data: GraduationCreate, db: Session = Depends(get_db)):
    crud = GraduationCrud(db)
    return crud.update_graduation(graduation_id, data)


@router.patch("/{graduation_id}", status_code=204)
def archive_graduation(graduation_id: UUID, reason: ArchiveRequest, db: Session = Depends(get_db)):
    crud = GraduationCrud(db)
    return crud.archive_graduation(graduation_id, reason.reason)


@router.delete("/{graduation_id}", status_code=204)
def delete_graduation(graduation_id: UUID, db: Session = Depends(get_db)):
    crud = GraduationCrud(db)
    return crud.delete_graduation(graduation_id)
