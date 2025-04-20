from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import Query
from typing import Annotated

from V2.app.core.shared.database.session_manager import get_db
from V2.app.core.staff_management.crud.staff_department import StaffDepartmentCrud
from V2.app.core.staff_management.schemas.department import StaffDepartmentResponse, DepartmentFilterParams
from fastapi import Depends, APIRouter



router = APIRouter()


@router.get("/", response_model=list[StaffDepartmentResponse])
def get_archived_staff_departments(filters: Annotated[DepartmentFilterParams, Query()],
        db: Session = Depends(get_db)):
    staff_departments_crud = StaffDepartmentCrud(db)
    return staff_departments_crud.get_all_archived_departments(filters)


@router.get("/{department_id}", response_model=StaffDepartmentResponse)
def get_archived_staff_department(department_id: UUID, db: Session = Depends(get_db)):
    staff_departments_crud = StaffDepartmentCrud(db)
    return staff_departments_crud.get_archived_department(department_id)


@router.patch("/{department_id}", response_model=StaffDepartmentResponse)
def restore_department(department_id: UUID,db: Session = Depends(get_db)):
    staff_departments_crud = StaffDepartmentCrud(db)
    return staff_departments_crud.restore_department(department_id)


@router.delete("/{department_id}", status_code=204)
def delete_archived_department(department_id: UUID, db: Session = Depends(get_db)):
    staff_departments_crud = StaffDepartmentCrud(db)
    return staff_departments_crud.delete_archived_department(department_id)










