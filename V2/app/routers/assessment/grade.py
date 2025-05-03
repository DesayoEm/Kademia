from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.assessment.crud.grade import GradeCrud
from V2.app.core.assessment.schemas.grade import (
    GradeCreate, GradeFilterParams, GradeUpdate, GradeResponse
)

router = APIRouter()

@router.post("/", response_model= GradeResponse, status_code=201)
def create_grade(data:GradeCreate,
                            db: Session = Depends(get_db)):
    grade_crud = GradeCrud(db)
    return grade_crud.create_grade(data)


@router.get("/", response_model=list[GradeResponse])
def get_grades(filters: GradeFilterParams = Depends(),db: Session = Depends(get_db)):
    grade_crud = GradeCrud(db)
    return grade_crud.get_all_grades(filters)


@router.get("/{level_id}", response_model=GradeResponse)
def get_grade(level_id: UUID, db: Session = Depends(get_db)):
    grade_crud = GradeCrud(db)
    return grade_crud.get_grade(level_id)


@router.put("/{level_id}", response_model=GradeResponse)
def update_grade(data: GradeUpdate, level_id: UUID,
                            db: Session = Depends(get_db)):
    grade_crud = GradeCrud(db)
    return grade_crud.update_grade(level_id, data)


@router.patch("/{level_id}",  status_code=204)
def archive_grade(level_id: UUID, reason:ArchiveRequest,
                       db: Session = Depends(get_db)):
    grade_crud = GradeCrud(db)
    return grade_crud.archive_grade(level_id, reason.reason)


@router.post("/{level_id}", response_class=FileResponse,  status_code=204)
def export_grade(level_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    grade_crud = GradeCrud(db)
    file_path= grade_crud.export_grade(level_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{level_id}", status_code=204)
def delete_grade(level_id: UUID, db: Session = Depends(get_db)):
    grade_crud = GradeCrud(db)
    return grade_crud.delete_grade(level_id)










