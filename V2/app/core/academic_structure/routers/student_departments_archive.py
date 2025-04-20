from sqlalchemy.orm import Session
from uuid import UUID

from V2.app.core.academic_structure.schemas.department import(
     DepartmentFilterParams, DepartmentResponse
)
from fastapi import Depends, APIRouter
from V2.app.core.shared.database import get_db
from V2.app.core.academic_structure.crud.student_departments import DepartmentCrud
from fastapi import Query
from typing import Annotated


router = APIRouter()


@router.get("/", response_model=list[DepartmentResponse])
def get_archived_departments(filters: Annotated[DepartmentFilterParams, Query()],
                                   db: Session = Depends(get_db)):
    student_departments_crud = DepartmentCrud(db)
    return student_departments_crud.get_all_archived_departments(filters)


@router.get("/{department_id}", response_model=DepartmentResponse)
def get_archived_department(department_id: UUID, db: Session = Depends(get_db)):
    student_departments_crud = DepartmentCrud(db)
    return student_departments_crud.get_archived_department(department_id)


@router.patch("/{department_id}", response_model=DepartmentResponse)
def restore_department(department_id: UUID,db: Session = Depends(get_db)):
    student_departments_crud = DepartmentCrud(db)
    return student_departments_crud.restore_department(department_id)


@router.delete("/{department_id}", status_code=204)
def delete_archived_department(department_id: UUID, db: Session = Depends(get_db)):
    student_departments_crud = DepartmentCrud(db)
    return student_departments_crud.delete_archived_department(department_id)




