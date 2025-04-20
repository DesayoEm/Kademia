from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.responses import FileResponse
from fastapi import Query
from typing import Annotated

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.core.shared.database.session_manager import get_db
from V2.app.core.academic_structure.crud.student_departments import DepartmentCrud
from V2.app.core.academic_structure.schemas.department import(
    DepartmentCreate, DepartmentUpdate, DepartmentFilterParams, DepartmentResponse
)

router = APIRouter()


@router.post("/", response_model= DepartmentResponse, status_code=201)
def create_department(data:DepartmentCreate,
                            db: Session = Depends(get_db)):
    student_departments_crud = DepartmentCrud(db)
    return student_departments_crud.create_department(data)


@router.get("/", response_model=list[DepartmentResponse])
def get_departments(filters: Annotated[DepartmentFilterParams, Query()],
                          db: Session = Depends(get_db)):
    student_departments_crud = DepartmentCrud(db)
    return student_departments_crud.get_all_departments(filters)


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(department_id: UUID, db: Session = Depends(get_db)):
    student_departments_crud = DepartmentCrud(db)
    return student_departments_crud.get_department(department_id)



@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(data: DepartmentUpdate, department_id: UUID,
                            db: Session = Depends(get_db)):
    student_departments_crud = DepartmentCrud(db)
    return student_departments_crud.update_department(department_id, data)


@router.patch("/{department_id}",  status_code=204)
def archive_department(department_id: UUID, reason:ArchiveRequest,
                       db: Session = Depends(get_db)):
    student_departments_crud = DepartmentCrud(db)
    return student_departments_crud.archive_department(department_id, reason.reason)


@router.post("/{department_id}", response_class=FileResponse,  status_code=204)
def export_department(department_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    student_departments_crud = DepartmentCrud(db)
    file_path= student_departments_crud.export_department(department_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{department_id}", status_code=204)
def delete_department(department_id: UUID, db: Session = Depends(get_db)):
    student_departments_crud = DepartmentCrud(db)
    return student_departments_crud.delete_department(department_id)










