from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.curriculum.crud.student_subject import StudentSubjectCrud
from V2.app.core.curriculum.schemas.student_subject import(
    StudentSubjectCreate, StudentSubjectFilterParams, StudentSubjectResponse
)


router = APIRouter()

@router.post("/", response_model= StudentSubjectResponse, status_code=201)
def assign_student_subject(data:StudentSubjectCreate,db: Session = Depends(get_db)):
    student_subject_crud = StudentSubjectCrud(db)
    return student_subject_crud.create_student_subject(data)


@router.get("/", response_model=List[StudentSubjectResponse])
def get_student_subjects(filters: StudentSubjectFilterParams = Depends(),db: Session = Depends(get_db)):
    student_subject_crud = StudentSubjectCrud(db)
    return student_subject_crud.get_all_student_subjects(filters)


@router.get("/{student_subject_id}", response_model=StudentSubjectResponse)
def get_student_subject(student_subject_id: UUID, db: Session = Depends(get_db)):
    student_subject_crud = StudentSubjectCrud(db)
    return student_subject_crud.get_student_subject(student_subject_id)



@router.patch("/{student_subject_id}",  status_code=204)
def archive_student_subject(student_subject_id: UUID, reason:ArchiveRequest,
                       db: Session = Depends(get_db)):
    student_subject_crud = StudentSubjectCrud(db)
    return student_subject_crud.archive_student_subject(student_subject_id, reason.reason)


@router.post("/{student_subject_id}", response_class=FileResponse,  status_code=204)
def export_student_subject(student_subject_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    student_subject_crud = StudentSubjectCrud(db)
    file_path= student_subject_crud.export_student_subject(student_subject_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{student_subject_id}", status_code=204)
def delete_student_subject(student_subject_id: UUID, db: Session = Depends(get_db)):
    student_subject_crud = StudentSubjectCrud(db)
    return student_subject_crud.delete_student_subject(student_subject_id)










