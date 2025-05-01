from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import Query
from typing import Annotated
from fastapi import Depends, APIRouter
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.identity.schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentFilterParams
from V2.app.infra.db.session_manager import get_db
from V2.app.core.identity.crud.student import StudentCrud
from V2.app.core.shared.schemas.shared_models import ArchiveRequest


router = APIRouter()


@router.post("/", response_model= StudentResponse, status_code=201)
def create_student(data:StudentCreate,
                db: Session = Depends(get_db)):
        student_crud = StudentCrud(db)
        return student_crud.create_student(data)


@router.get("/", response_model=list[StudentResponse])
def get_students(filters: StudentFilterParams = Depends(),db: Session = Depends(get_db)):
        student_crud = StudentCrud(db)
        return student_crud.get_all_students(filters)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: UUID, db: Session = Depends(get_db)):
        student_crud = StudentCrud(db)
        return student_crud.get_student(student_id)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(data: StudentUpdate, student_id: UUID,
                         db: Session = Depends(get_db)):
        student_crud = StudentCrud(db)
        return student_crud.update_student(student_id, data)


@router.patch("/{student_id}", status_code=204)
def archive_student(student_id: UUID, reason:ArchiveRequest,
                          db: Session = Depends(get_db)):
        student_crud = StudentCrud(db)
        return student_crud.archive_student(student_id, reason.reason)


@router.post("/{student_id}", response_class=FileResponse,  status_code=204)
def export_student(student_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    file_path= student_crud.export_student(student_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: UUID, db: Session = Depends(get_db)):
        student_crud = StudentCrud(db)
        return student_crud.delete_student(student_id)











