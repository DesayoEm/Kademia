from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from uuid import UUID
from V2.app.core.assessment.schemas.total_grade import TotalGradeFilterParams, TotalGradeResponse
from V2.app.infra.db.session_manager import get_db
from V2.app.core.assessment.crud.total_grade import TotalGradeCrud


router = APIRouter()


@router.get("/", response_model=list[TotalGradeResponse])
def get_archived_total_grades(filters: TotalGradeFilterParams = Depends(),db: Session = Depends(get_db)):
    total_grades_crud = TotalGradeCrud(db)
    return total_grades_crud.get_all_archived_total_grades(filters)


@router.get("/{total_grade_id}", response_model=TotalGradeResponse)
def get_archived_total_grade(total_grade_id: UUID, db: Session = Depends(get_db)):
    total_grades_crud = TotalGradeCrud(db)
    return total_grades_crud.get_archived_total_grade(total_grade_id)


@router.patch("/{total_grade_id}", response_model=TotalGradeResponse)
def restore_total_grade(total_grade_id: UUID,db: Session = Depends(get_db)):
    total_grades_crud = TotalGradeCrud(db)
    return total_grades_crud.restore_total_grade(total_grade_id)


@router.delete("/{total_grade_id}", status_code=204)
def delete_archived_total_grade(total_grade_id: UUID, db: Session = Depends(get_db)):
    total_grades_crud = TotalGradeCrud(db)
    return total_grades_crud.delete_archived_total_grade(total_grade_id)




