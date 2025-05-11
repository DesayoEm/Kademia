
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.core.assessment.crud.grade import GradeCrud
from V2.app.core.assessment.schemas.grade import (
    GradeCreate, GradeFilterParams, GradeUpdate, GradeResponse
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/{student_subject_id}", response_model= GradeResponse, status_code=201)
def grade_student(
        student_subject_id: UUID,
        data:GradeCreate,
        crud: GradeCrud = Depends(get_authenticated_crud(GradeCrud))
    ):
    return crud.create_grade(student_subject_id, data)


@router.get("/", response_model=List[GradeResponse])
def get_grades(
        filters: GradeFilterParams = Depends(),
        crud: GradeCrud = Depends(get_authenticated_crud(GradeCrud))
    ):
    return crud.get_all_grades(filters)


@router.get("/student-subject/{grade_id}", response_model=GradeResponse)
def get_grade(
        grade_id: UUID,
        crud: GradeCrud = Depends(get_authenticated_crud(GradeCrud))
    ):
    return crud.get_grade(grade_id)


@router.put("/{grade_id}", response_model=GradeResponse)
def update_grade(
        data: GradeUpdate,
        grade_id: UUID,
        crud: GradeCrud = Depends(get_authenticated_crud(GradeCrud))
    ):
    return crud.update_grade(grade_id, data)


@router.patch("/{grade_id}",  status_code=204)
def archive_grade(
        grade_id: UUID,
        reason:ArchiveRequest,
        crud: GradeCrud = Depends(get_authenticated_crud(GradeCrud))
    ):
    return crud.archive_grade(grade_id, reason.reason)


@router.get("/{grade_id}/export", response_class=FileResponse,  status_code=200)
def export_grade(
        grade_id: UUID,
        export_format: ExportFormat,
        crud: GradeCrud = Depends(get_authenticated_crud(GradeCrud))
    ):
    file_path= crud.export_grade(grade_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{grade_id}", status_code=204)
def delete_grade(
        grade_id: UUID,
        crud: GradeCrud = Depends(get_authenticated_crud(GradeCrud))
    ):
    return crud.delete_grade(grade_id)










