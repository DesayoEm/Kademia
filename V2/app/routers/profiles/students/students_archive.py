from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ...database.utils import get_db
from ...crud.students import ArchivedStudentService
from ...services.exceptions.profiles import ArchivedStudentNotFound, NoArchiveRecords
from fastapi import HTTPException

router = APIRouter()

@router.get("/")
def get_students(db: Session = Depends(get_db)):
    archived = ArchivedStudentService(db)
    try:
        return archived.get_archived_students()
    except NoArchiveRecords as e:
        raise HTTPException(status_code = 404, detail = str(e))


@router.get("/{student_id}")
def get_student(stu_id: str, db: Session = Depends(get_db)):
    archived = ArchivedStudentService(db)
    try:
        return archived.get_archived_student(stu_id)
    except ArchivedStudentNotFound as e:
        raise HTTPException(status_code = 404, detail = str(e))


@router.patch("/{student_id}")
def restore_student(stu_id: str, db: Session = Depends(get_db)):
    archived = ArchivedStudentService(db)
    try:
        return archived.restore_student(stu_id)
    except ArchivedStudentNotFound as e:
        raise HTTPException(status_code = 404, detail = str(e))


@router.delete("/{student_id}")
def delete_archived_student(stu_id: str, db: Session = Depends(get_db)):
    archived = ArchivedStudentService(db)
    try:
        return archived.delete_archived_student(stu_id)
    except ArchivedStudentNotFound as e:
        raise HTTPException(status_code = 404, detail = str(e))