from sqlalchemy.orm import Session
from uuid import UUID

from ...database.models.data_enums import ArchiveReason
from ...schemas.staff_organization.educator_qualifications import(
    QualificationCreate, QualificationUpdate, QualificationResponse, QualificationFilterParams
)
from fastapi import Depends, APIRouter
from ...database.session_manager import get_db
from ...crud.staff_organization.educator_qualifications import QualificationsCrud
from fastapi import HTTPException, Query
from typing import Annotated

from ...services.errors.database_errors import (
    EntityNotFoundError, DatabaseError,
)
router = APIRouter()


@router.post("/", response_model= QualificationResponse)
def create_qualification(
        data:QualificationCreate,
        db: Session = Depends(get_db)):
    try:
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.create_qualification(data)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=list[QualificationResponse])
def get_qualifications(
        filters: Annotated[QualificationFilterParams, Query()],
        db: Session = Depends(get_db)):
    try:
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.get_all_qualifications(filters)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{qualification_id}", response_model=QualificationResponse)
def get_qualification(qualification_id: UUID, db: Session = Depends(get_db)):
    try:
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.get_qualification(qualification_id)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{qualification_id}", response_model=QualificationResponse)
def update_qualification(data: QualificationUpdate, qualification_id: UUID,
                         db: Session = Depends(get_db)):
    try:
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.update_qualification(qualification_id, data)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{qualification_id}", response_model=QualificationResponse)
def archive_qualification(qualification_id: UUID, reason:ArchiveReason,
                          db: Session = Depends(get_db)):
    try:
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.archive_qualification(qualification_id, reason)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{qualification_id}", response_model=QualificationResponse)
def delete_qualification(qualification_id: UUID, db: Session = Depends(get_db)):
    try:
        qualifications_crud = QualificationsCrud(db)
        return qualifications_crud.delete_qualification(qualification_id)
    except DatabaseError as e:
        raise HTTPException(status_code=404, detail=str(e))



















#
# @router.get("/{student_id}")
# def get_student(stu_id: str, db: Session = Depends(get_db)):
#     try:
#         student_crud = StudentCrud(db)
#         return student_crud.read_student(stu_id)
#     except StudentNotFoundError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#
#
# @router.post("/", status_code = 201)
# def create_student(new_student:NewStudent, db: Session = Depends(get_db)):
#     student_crud = StudentCrud(db)
#     try:
#         student_crud.create_student(new_student)
#     except DuplicateStudentIDError as e:
#         raise HTTPException(status_code=400, detail = str(e))
#     except StudentIdFormatError as e:
#         raise HTTPException(status_code=400, detail = str(e))
#     except IdYearError as e:
#         raise HTTPException(status_code=400, detail = str(e))
#     except AdmissionDateError as e:
#         raise HTTPException(status_code=400, detail = str(e))
#
#
# @router.put("/{student_id}")
# def update_student(stu_id: str, data:UpdateStudent, db: Session = Depends(get_db)):
#     student_crud = StudentCrud(db)
#     try:
#         return student_crud.update_student(stu_id, data)
#     except DuplicateStudentIDError as e:
#         raise HTTPException(status_code=400, detail = str(e))
#     except StudentIdFormatError as e:
#         raise HTTPException(status_code=400, detail = str(e))
#     except IdYearError as e:
#         raise HTTPException(status_code=400, detail = str(e))
#     except AdmissionDateError as e:
#         raise HTTPException(status_code=400, detail = str(e))
#
#
# @router.patch("/{student_id}")
# def archive_student(stu_id: str, reason: ArchiveReason, db: Session = Depends(get_db)):
#     student_crud = StudentCrud(db)
#     return student_crud.archive_student(stu_id, reason)
#
#
# @router.delete("/{student_id}", status_code = 204)
# def delete_student(stu_id: str, db: Session = Depends(get_db)):
#     student_crud = StudentCrud(db)
#     return student_crud.delete_student(stu_id)
#
