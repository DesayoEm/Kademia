from sqlalchemy.orm import Session
from uuid import UUID

from ...schemas.student_organization.academic_level import(
    AcademicLevelCreate, AcademicLevelUpdate, AcademicLevelFilterParams, AcademicLevelResponse
)
from ...schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from ...database.session import get_db
from ...crud.student_organization.academic_levels import AcademicLevelCrud
from fastapi import Query
from typing import Annotated


router = APIRouter()

@router.post("/", response_model= AcademicLevelResponse, status_code=201)
def create_level(data:AcademicLevelCreate,
                            db: Session = Depends(get_db)):
    academic_level_crud = AcademicLevelCrud(db)
    return academic_level_crud.create_level(data)


@router.get("/", response_model=list[AcademicLevelResponse])
def get_levels(filters: Annotated[AcademicLevelFilterParams, Query()],
                          db: Session = Depends(get_db)):
    academic_level_crud = AcademicLevelCrud(db)
    return academic_level_crud.get_all_levels(filters)


@router.get("/{level_id}", response_model=AcademicLevelResponse)
def get_level(level_id: UUID, db: Session = Depends(get_db)):
    academic_level_crud = AcademicLevelCrud(db)
    return academic_level_crud.get_level(level_id)


@router.put("/{level_id}", response_model=AcademicLevelResponse)
def update_level(data: AcademicLevelUpdate, level_id: UUID,
                            db: Session = Depends(get_db)):
    academic_level_crud = AcademicLevelCrud(db)
    return academic_level_crud.update_level(level_id, data)


@router.patch("/{level_id}",  status_code=204)
def archive_level(level_id: UUID, reason:ArchiveRequest,
                       db: Session = Depends(get_db)):
    academic_level_crud = AcademicLevelCrud(db)
    return academic_level_crud.archive_level(level_id, reason.reason)


@router.delete("/{level_id}", status_code=204)
def delete_level(level_id: UUID, db: Session = Depends(get_db)):
    academic_level_crud = AcademicLevelCrud(db)
    return academic_level_crud.delete_level(level_id)










