from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.curriculum.crud.academic_level_subject import AcademicLevelSubjectCrud
from V2.app.core.curriculum.schemas.academic_level_subject import(
    AcademicLevelSubjectCreate, AcademicLevelSubjectFilterParams, AcademicLevelSubjectResponse
)


router = APIRouter()

@router.post("/", response_model= AcademicLevelSubjectResponse, status_code=201)
def assign_level_subject(data:AcademicLevelSubjectCreate,db: Session = Depends(get_db)):
    level_subject_crud = AcademicLevelSubjectCrud(db)
    return level_subject_crud.create_level_subject(data)


@router.get("/", response_model=List[AcademicLevelSubjectResponse])
def get_level_subjects(filters: AcademicLevelSubjectFilterParams = Depends(),db: Session = Depends(get_db)):
    level_subject_crud = AcademicLevelSubjectCrud(db)
    return level_subject_crud.get_all_level_subjects(filters)


@router.get("/{level_subject_id}", response_model=AcademicLevelSubjectResponse)
def get_level_subject(level_subject_id: UUID, db: Session = Depends(get_db)):
    level_subject_crud = AcademicLevelSubjectCrud(db)
    return level_subject_crud.get_level_subject(level_subject_id)



@router.patch("/{level_subject_id}",  status_code=204)
def archive_level_subject(level_subject_id: UUID, reason:ArchiveRequest,
                       db: Session = Depends(get_db)):
    level_subject_crud = AcademicLevelSubjectCrud(db)
    return level_subject_crud.archive_level_subject(level_subject_id, reason.reason)


@router.post("/{level_subject_id}", response_class=FileResponse,  status_code=204)
def export_level_subject(level_subject_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    level_subject_crud = AcademicLevelSubjectCrud(db)
    file_path= level_subject_crud.export_level_subject(level_subject_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{level_subject_id}", status_code=204)
def delete_level_subject(level_subject_id: UUID, db: Session = Depends(get_db)):
    level_subject_crud = AcademicLevelSubjectCrud(db)
    return level_subject_crud.delete_level_subject(level_subject_id)










