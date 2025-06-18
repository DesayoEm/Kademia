

from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.curriculum.factories.academic_level_subject import AcademicLevelSubjectFactory
from V2.app.core.curriculum.services.curriculum_service import CurriculumService
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.core.curriculum.schemas.academic_level_subject import(
    AcademicLevelSubjectCreate, AcademicLevelSubjectFilterParams, AcademicLevelSubjectResponse,
    AcademicLevelSubjectAudit
)

from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory,\
    get_authenticated_service

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/{level_id}", response_model= AcademicLevelSubjectResponse, status_code=201)
def assign_level_subject(
        level_id: UUID,
        payload:AcademicLevelSubjectCreate,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.create_academic_level_subject(level_id, payload)


@router.get("/", response_model=List[AcademicLevelSubjectResponse])
def get_level_subjects(
        filters: AcademicLevelSubjectFilterParams = Depends(),
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.get_all_academic_level_subjects(filters)


@router.get("/{level_subject_id}/audit", response_model=AcademicLevelSubjectAudit)
def get_level_subject_audit(
        level_subject_id: UUID,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.get_academic_level_subject(level_subject_id)



@router.get("/{level_subject_id}", response_model=AcademicLevelSubjectResponse)
def get_level_subject(
        level_subject_id: UUID,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.get_academic_level_subject(level_subject_id)


@router.patch("/{level_subject_id}",  status_code=204)
def archive_level_subject(
        level_subject_id: UUID,
        reason:ArchiveRequest,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.archive_academic_level_subject(level_subject_id, reason.reason)


@router.post("/{level_subject_id}", response_class=FileResponse,  status_code=204)
def export_level_subject(
        level_subject_id: UUID,
        export_format: ExportFormat,
        service: CurriculumService = Depends(get_authenticated_service(CurriculumService))
    ):
    file_path= service.export_level_subject_audit(level_subject_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{level_subject_id}", status_code=204)
def delete_level_subject(
        level_subject_id: UUID,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.delete_academic_level_subject(level_subject_id)










