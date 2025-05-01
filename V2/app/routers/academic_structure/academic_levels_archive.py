from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from uuid import UUID

from V2.app.core.academic_structure.schemas.academic_level import(
    AcademicLevelFilterParams, AcademicLevelResponse
)
from V2.app.infra.db.session_manager import get_db
from V2.app.core.academic_structure.crud.academic_levels import AcademicLevelCrud



router = APIRouter()


@router.get("/", response_model=list[AcademicLevelResponse])
def get_archived_levels(filters: AcademicLevelFilterParams = Depends(),db: Session = Depends(get_db)):
    academic_levels_crud = AcademicLevelCrud(db)
    return academic_levels_crud.get_all_archived_levels(filters)


@router.get("/{level_id}", response_model=AcademicLevelResponse)
def get_archived_level(level_id: UUID, db: Session = Depends(get_db)):
    academic_levels_crud = AcademicLevelCrud(db)
    return academic_levels_crud.get_archived_level(level_id)


@router.patch("/{level_id}", response_model=AcademicLevelResponse)
def restore_level(level_id: UUID,db: Session = Depends(get_db)):
    academic_levels_crud = AcademicLevelCrud(db)
    return academic_levels_crud.restore_level(level_id)


@router.delete("/{level_id}", status_code=204)
def delete_archived_level(department_id: UUID, db: Session = Depends(get_db)):
    academic_levels_crud = AcademicLevelCrud(db)
    return academic_levels_crud.delete_archived_level(department_id)




