from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.responses import FileResponse
from fastapi import Query
from typing import Annotated

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.core.shared.database.session_manager import get_db
from V2.app.core.academic_structure.crud.academic_levels import AcademicLevelCrud
from V2.app.core.academic_structure.schemas.academic_level import(
    AcademicLevelCreate, AcademicLevelUpdate, AcademicLevelFilterParams, AcademicLevelResponse
)


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


@router.post("/{level_id}", response_class=FileResponse,  status_code=204)
def export_level(level_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    academic_level_crud = AcademicLevelCrud(db)
    file_path= academic_level_crud.export_level(level_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{level_id}", status_code=204)
def delete_level(level_id: UUID, db: Session = Depends(get_db)):
    academic_level_crud = AcademicLevelCrud(db)
    return academic_level_crud.delete_level(level_id)










