from sqlalchemy.orm import Session

from ...database.models.data_enums import ArchiveReason
from ...schemas.profiles import NewStudent, UpdateStudent, Student
from fastapi import Depends, APIRouter
from ...database.utils import get_db
from ...crud.students import StudentCrud
from fastapi import HTTPException
from ...services.exceptions.profiles import (
    StudentNotFoundError, IdYearError, StudentIdFormatError,
    AdmissionDateError, DuplicateStudentIDError)

router = APIRouter()


@router.get("/", response_model = list[Student])
def get_students(db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.read_all_students()


@router.get("/{student_id}")
def get_student(stu_id: str, db: Session = Depends(get_db)):
    try:
        student_crud = StudentCrud(db)
        return student_crud.read_student(stu_id)
    except StudentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", status_code = 201)
def create_student(new_student:NewStudent, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    try:
       student_crud.create_student(new_student)
    except DuplicateStudentIDError as e:
        raise HTTPException(status_code=400, detail = str(e))
    except StudentIdFormatError as e:
        raise HTTPException(status_code=400, detail = str(e))
    except IdYearError as e:
        raise HTTPException(status_code=400, detail = str(e))
    except AdmissionDateError as e:
        raise HTTPException(status_code=400, detail = str(e))


@router.put("/{student_id}")
def update_student(stu_id: str, data:UpdateStudent, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    try:
        return student_crud.update_student(stu_id, data)
    except DuplicateStudentIDError as e:
        raise HTTPException(status_code=400, detail = str(e))
    except StudentIdFormatError as e:
        raise HTTPException(status_code=400, detail = str(e))
    except IdYearError as e:
        raise HTTPException(status_code=400, detail = str(e))
    except AdmissionDateError as e:
        raise HTTPException(status_code=400, detail = str(e))



@router.patch("/{student_id}")
def archive_student(stu_id: str, reason: ArchiveReason, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.archive_student(stu_id, reason)


@router.delete("/{student_id}", status_code = 204)
def delete_student(stu_id: str, db: Session = Depends(get_db)):
    student_crud = StudentCrud(db)
    return student_crud.delete_student(stu_id)

