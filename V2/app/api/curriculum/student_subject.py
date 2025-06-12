
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter

from V2.app.core.curriculum.crud.student_subject import StudentSubjectCrud
from V2.app.core.curriculum.schemas.student_subject import(
    StudentSubjectCreate, StudentSubjectFilterParams, StudentSubjectResponse
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/{student_id}", response_model= StudentSubjectResponse, status_code=201)
def assign_student_subject(
        student_id: UUID,
        payload:StudentSubjectCreate,
        crud: StudentSubjectCrud = Depends(get_authenticated_crud(StudentSubjectCrud))
    ):
    return crud.create_student_subject(student_id, payload)


@router.get("/", response_model=List[StudentSubjectResponse])
def get_student_subjects(
        filters: StudentSubjectFilterParams = Depends(),
        crud: StudentSubjectCrud = Depends(get_authenticated_crud(StudentSubjectCrud))
    ):
    return crud.get_all_student_subjects(filters)


@router.get("/{student_subject_id}", response_model=StudentSubjectResponse)
def get_student_subject(
        student_subject_id: UUID,
        crud: StudentSubjectCrud = Depends(get_authenticated_crud(StudentSubjectCrud))
    ):
    return crud.get_student_subject(student_subject_id)


@router.patch("/{student_subject_id}",  status_code=204)
def archive_student_subject(
        student_subject_id: UUID,
        reason:ArchiveRequest,
        crud: StudentSubjectCrud = Depends(get_authenticated_crud(StudentSubjectCrud))
    ):
    
    return crud.archive_student_subject(student_subject_id, reason.reason)


@router.post("/{student_subject_id}", response_class=FileResponse,  status_code=204)
def export_student_subject(
        student_subject_id: UUID,
        export_format: ExportFormat,
        crud: StudentSubjectCrud = Depends(get_authenticated_crud(StudentSubjectCrud))
    ):
    
    file_path= crud.export_student_subject(student_subject_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{student_subject_id}", status_code=204)
def delete_student_subject(
        student_subject_id: UUID,
        crud: StudentSubjectCrud = Depends(get_authenticated_crud(StudentSubjectCrud))
    ):
    return crud.delete_student_subject(student_subject_id)










