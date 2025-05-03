from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from uuid import UUID
from V2.app.core.assessment.schemas.grade import GradeFilterParams, GradeResponse
from V2.app.infra.db.session_manager import get_db
from V2.app.core.assessment.crud.grade import GradeCrud


router = APIRouter()


@router.get("/", response_model=list[GradeResponse])
def get_archived_grades(filters: GradeFilterParams = Depends(),db: Session = Depends(get_db)):
    grades_crud = GradeCrud(db)
    return grades_crud.get_all_archived_grades(filters)


@router.get("/{total_grade_id}", response_model=GradeResponse)
def get_archived_grade(total_grade_id: UUID, db: Session = Depends(get_db)):
    grades_crud = GradeCrud(db)
    return grades_crud.get_archived_grade(total_grade_id)


@router.patch("/{total_grade_id}", response_model=GradeResponse)
def restore_total_grade(total_grade_id: UUID,db: Session = Depends(get_db)):
    grades_crud = GradeCrud(db)
    return grades_crud.restore_grade(total_grade_id)


@router.delete("/{total_grade_id}", status_code=204)
def delete_archived_grade(total_grade_id: UUID, db: Session = Depends(get_db)):
    grades_crud = GradeCrud(db)
    return grades_crud.delete_archived_grade(total_grade_id)




