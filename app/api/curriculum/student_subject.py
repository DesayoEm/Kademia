import io
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse
from starlette.responses import StreamingResponse

from app.core.shared.schemas.enums import Term
from app.core.curriculum.factories.student_subject import StudentSubjectFactory
from app.core.curriculum.schemas.curriculum import CourseListRequest, CourseListResponse
from app.core.curriculum.services.curriculum_service import CurriculumService

from app.core.shared.schemas.enums import ExportFormat
from app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter

from app.core.curriculum.schemas.student_subject import (
    StudentSubjectCreate, StudentSubjectFilterParams, StudentSubjectResponse, StudentSubjectAudit
)
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/{student_id}", response_model= StudentSubjectResponse, status_code=201)
def assign_student_subject(
        student_id: UUID,
        payload:StudentSubjectCreate,
        factory: StudentSubjectFactory = Depends(get_authenticated_factory(StudentSubjectFactory))
    ):
    return factory.create_student_subject(student_id, payload)

@router.get("/students/{student_id}/course_list/download")
def download_course_list(
        student_id: UUID,
        academic_session: str,
        term: Term,
        service: CurriculumService = Depends(get_authenticated_service(CurriculumService))
):
    pdf_bytes, filename = service.render_course_list_pdf(student_id, academic_session, term)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type = "application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@router.post("/students/{student_id}/course_list", response_model=CourseListResponse)
def get_student_course_list(
        student_id: UUID,
        payload: CourseListRequest,
        service: CurriculumService = Depends(get_authenticated_service(CurriculumService))
    ):
    return service.generate_student_course_list(
        student_id, payload.academic_session, payload.term
    )


@router.get("/", response_model=List[StudentSubjectResponse])
def get_student_subjects(
        filters: StudentSubjectFilterParams = Depends(),
        factory: StudentSubjectFactory = Depends(get_authenticated_factory(StudentSubjectFactory))
    ):
    return factory.get_all_student_subjects(filters)


@router.get("/{student_subject_id}/audit", response_model=StudentSubjectAudit)
def get_student_subject_audit(
        student_subject_id: UUID,
        factory: StudentSubjectFactory = Depends(get_authenticated_factory(StudentSubjectFactory))
    ):
    return factory.get_student_subject(student_subject_id)


@router.get("/{student_subject_id}", response_model=StudentSubjectResponse)
def get_student_subject(
        student_subject_id: UUID,
        factory: StudentSubjectFactory = Depends(get_authenticated_factory(StudentSubjectFactory))
    ):
    return factory.get_student_subject(student_subject_id)


@router.patch("/{student_subject_id}",  status_code=204)
def archive_student_subject(
        student_subject_id: UUID,
        reason:ArchiveRequest,
        factory: StudentSubjectFactory = Depends(get_authenticated_factory(StudentSubjectFactory))
    ):
    
    return factory.archive_student_subject(student_subject_id, reason.reason)



@router.delete("/{student_subject_id}", status_code=204)
def delete_student_subject(
        student_subject_id: UUID,
        factory: StudentSubjectFactory = Depends(get_authenticated_factory(StudentSubjectFactory))
    ):
    return factory.delete_student_subject(student_subject_id)










