
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse
from fastapi import UploadFile, File

from V2.app.core.assessment.services.assessment_file_service import AssessmentFileService
from V2.app.core.assessment.services.assessment_service import AssessmentService
from V2.app.core.identity.factories.student import StudentFactory
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest, UploadResponse
from V2.app.core.assessment.factories.grade import GradeFactory
from fastapi import Depends, APIRouter
from V2.app.core.assessment.schemas.grade import (
    GradeCreate, GradeFilterParams, GradeUpdate, GradeResponse, GradeAudit
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()

@router.post("/{student_id}/assessments/{grade_id}/file", response_model= UploadResponse,
             status_code=201)
def upload_assessment_file(
        grade_id: UUID,
        student_id: UUID,
        file: UploadFile = File(...),
        service: AssessmentFileService = Depends(get_authenticated_service(AssessmentFileService)),
        grade_factory: GradeFactory = Depends(get_authenticated_factory(GradeFactory)),
        student_factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
        grade = grade_factory.get_grade(grade_id)
        student = student_factory.get_student(student_id)
        result = service.upload_assessment_file(file, student, grade)

        return UploadResponse(**result)

@router.post("/{student_subject_id}", response_model= GradeResponse, status_code=201)
def grade_student(
        student_id: UUID,
        student_subject_id: UUID,
        payload:GradeCreate,
        factory: GradeFactory = Depends(get_authenticated_factory(GradeFactory))
    ):
    return factory.create_grade(student_id, student_subject_id, payload)


@router.get("/", response_model=List[GradeResponse])
def get_grades(
        filters: GradeFilterParams = Depends(),
        factory: GradeFactory = Depends(get_authenticated_factory(GradeFactory))
    ):
    return factory.get_all_grades(filters)


@router.get("/student-subject/{grade_id}/audit", response_model=GradeAudit)
def get_grade_audit(
        grade_id: UUID,
        factory: GradeFactory = Depends(get_authenticated_factory(GradeFactory))
    ):
    return factory.get_grade(grade_id)


@router.get("/student-subject/{grade_id}", response_model=GradeResponse)
def get_grade(
        grade_id: UUID,
        factory: GradeFactory = Depends(get_authenticated_factory(GradeFactory))
    ):
    return factory.get_grade(grade_id)


@router.put("/{grade_id}", response_model=GradeResponse)
def update_grade(
        payload: GradeUpdate,
        grade_id: UUID,
        service: AssessmentService = Depends(get_authenticated_service(AssessmentService))
    ):
    payload = payload.model_dump(exclude_unset=True)
    return service.handle_grade_update(grade_id, payload)


@router.patch("/{grade_id}",  status_code=204)
def archive_grade(
        grade_id: UUID,
        reason:ArchiveRequest,
        factory: GradeFactory = Depends(get_authenticated_factory(GradeFactory))
    ):
    return factory.archive_grade(grade_id, reason.reason)


@router.get("/{grade_id}/audit/export", response_class=FileResponse,  status_code=200)
def export_grade_audit(
        grade_id: UUID,
        export_format: ExportFormat,
        service: AssessmentService = Depends(get_authenticated_service(AssessmentService))
    ):
    file_path= service.export_grade_audit(grade_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{grade_id}", status_code=204)
def delete_grade(
        grade_id: UUID,
        factory: GradeFactory = Depends(get_authenticated_factory(GradeFactory))
    ):
    return factory.delete_grade(grade_id)










