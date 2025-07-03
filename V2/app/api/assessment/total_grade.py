
from fastapi import Depends, APIRouter
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.assessment.services.assessment_service import AssessmentService
from V2.app.core.shared.schemas.enums import ExportFormat


from V2.app.core.assessment.schemas.total_grade import TotalGradeFilterParams, TotalGradeResponse, TotalGradeAudit
from V2.app.core.assessment.factories.total_grade import TotalGradeFactory
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/{student_subject_id}", response_model= TotalGradeResponse, status_code=201)
def generate_total_grade(
        student_subject_id: UUID,
        factory: TotalGradeFactory = Depends(get_authenticated_factory(TotalGradeFactory))
    ):
    return factory.create_total_grade(student_subject_id)


@router.get("/", response_model=List[TotalGradeResponse])
def get_total_grades(
        filters: TotalGradeFilterParams = Depends(),
        factory: TotalGradeFactory = Depends(get_authenticated_factory(TotalGradeFactory))
    ):
    return factory.get_all_total_grades(filters)


@router.get("/{grade_id}/audit", response_model=TotalGradeAudit)
def get_total_grade_audit(
        grade_id: UUID,
        factory: TotalGradeFactory = Depends(get_authenticated_factory(TotalGradeFactory))
    ):
    return factory.get_total_grade(grade_id)


@router.get("/{grade_id}", response_model=TotalGradeResponse)
def get_total_grade(
        grade_id: UUID,
        factory: TotalGradeFactory = Depends(get_authenticated_factory(TotalGradeFactory))
    ):
    return factory.get_total_grade(grade_id)


@router.patch("/{grade_id}", response_model=TotalGradeResponse)
def restore_total_grade(
        grade_id: UUID,
        factory: TotalGradeFactory = Depends(get_authenticated_factory(TotalGradeFactory))
    ):
    return factory.restore_total_grade(grade_id)


@router.delete("/{grade_id}", status_code=204)
def delete_total_grade(
        grade_id: UUID,
        factory: TotalGradeFactory = Depends(get_authenticated_factory(TotalGradeFactory))
    ):
    return factory.delete_total_grade(grade_id)


@router.get("/{total_grade_id}/audit/export", response_class=FileResponse,  status_code=200)
def export_total_grade_audit(
        total_grade_id: UUID,
        export_format: ExportFormat,
        service: AssessmentService = Depends(get_authenticated_service(AssessmentService))
    ):
    file_path= service.export_total_grade_audit(total_grade_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )



