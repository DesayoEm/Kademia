from sqlalchemy.orm import Session
from uuid import UUID

from ...database.models.data_enums import ArchiveReason
from ...schemas.staff_organization.staff_departments import(
    StaffDepartmentCreate, StaffDepartmentUpdate, StaffDepartmentResponse, DepartmentFilterParams
)
from fastapi import Depends, APIRouter
from ...database.session_manager import get_db
from ...crud.staff_organization.staff_departments import StaffDepartmentCrud
from fastapi import HTTPException, Query
from typing import Annotated

from ...services.errors.database_errors import (
    EntityNotFoundError, DatabaseError,
)
router = APIRouter()


@router.post("/", response_model= StaffDepartmentResponse, status_code=201)
def create_staff_department(
        data:StaffDepartmentCreate,
        db: Session = Depends(get_db)):
    try:
        staff_departments_crud = StaffDepartmentCrud(db)
        return staff_departments_crud.create_department(data)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))



@router.get("/", response_model=list[StaffDepartmentResponse])
def get_staff_departments(
        filters: Annotated[DepartmentFilterParams, Query()],
        db: Session = Depends(get_db)):
    try:
        staff_departments_crud = StaffDepartmentCrud(db)
        return staff_departments_crud.get_all_departments(filters)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{department_id}", response_model=StaffDepartmentResponse)
def get_staff_department(department_id: UUID, db: Session = Depends(get_db)):
    try:
        staff_departments_crud = StaffDepartmentCrud(db)
        return staff_departments_crud.get_department(department_id)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{department_id}", response_model=StaffDepartmentResponse)
def update_staff_department(data: StaffDepartmentUpdate, department_id: UUID,
                         db: Session = Depends(get_db)):
    try:
        staff_departments_crud = StaffDepartmentCrud(db)
        return staff_departments_crud.update_department(department_id, data)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{department_id}", response_model=StaffDepartmentResponse)
def archive_department(department_id: UUID, reason:ArchiveReason,
                          db: Session = Depends(get_db)):
    try:
        staff_departments_crud = StaffDepartmentCrud(db)
        return staff_departments_crud.archive_department(department_id, reason)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{department_id}", status_code=204)
def delete_department(department_id: UUID, db: Session = Depends(get_db)):
    try:
        staff_departments_crud = StaffDepartmentCrud(db)
        return staff_departments_crud.delete_department(department_id)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))










