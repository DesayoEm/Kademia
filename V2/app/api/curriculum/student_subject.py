
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.curriculum.factories.student_subject import StudentSubjectFactory


from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter

from V2.app.core.curriculum.schemas.student_subject import (
    StudentSubjectCreate, StudentSubjectFilterParams, StudentSubjectResponse, StudentSubjectAudit
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

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


@router.post("/{student_subject_id}", response_class=FileResponse,  status_code=204)
def export_student_subject(
        student_subject_id: UUID,
        export_format: ExportFormat,
        factory: StudentSubjectFactory = Depends(get_authenticated_factory(StudentSubjectFactory))
    ):
    
    file_path= factory.export_student_subject(student_subject_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{student_subject_id}", status_code=204)
def delete_student_subject(
        student_subject_id: UUID,
        factory: StudentSubjectFactory = Depends(get_authenticated_factory(StudentSubjectFactory))
    ):
    return factory.delete_student_subject(student_subject_id)










