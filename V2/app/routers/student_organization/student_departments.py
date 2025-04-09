from sqlalchemy.orm import Session
from uuid import UUID

from ...schemas.student_organization.department import(
    DepartmentCreate, DepartmentUpdate, DepartmentFilterParams, DepartmentResponse
)
from ...schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from ...database.session import get_db
from ...crud.student_organization.student_departments import DepartmentCrud
from fastapi import Query
from typing import Annotated


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


@router.delete("/{department_id}", status_code=204)
def delete_department(department_id: UUID, db: Session = Depends(get_db)):
    student_departments_crud = DepartmentCrud(db)
    return student_departments_crud.delete_department(department_id)










