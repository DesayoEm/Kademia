

from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from app.core.curriculum.factories.academic_level_subject import AcademicLevelSubjectFactory
from app.core.curriculum.schemas.student_subject import StudentSubjectFilterParams
from app.core.curriculum.services.curriculum_service import CurriculumService
from app.core.identity.factories.student import StudentFactory
from app.core.identity.schemas.student import StudentResponse
from app.core.shared.schemas.enums import ExportFormat
from app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from app.core.curriculum.schemas.academic_level_subject import(
    AcademicLevelSubjectCreate, AcademicLevelSubjectFilterParams, AcademicLevelSubjectResponse,
    AcademicLevelSubjectAudit
)

from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory,\
    get_authenticated_service

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


#Archive routers
@router.get("/archive/level-subjects/", response_model=List[AcademicLevelSubjectResponse])
def get_archived_level_subjects(
        filters: AcademicLevelSubjectFilterParams = Depends(),
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.get_all_archived_academic_level_subjects(filters)


@router.get("/archive/level-subjects/{level_subject_id}", response_model=AcademicLevelSubjectResponse)
def get_archived_level_subject(
        level_subject_id: UUID,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.get_archived_academic_level_subject(level_subject_id)


@router.patch("/archive/level-subjects/{level_subject_id}", response_model=AcademicLevelSubjectResponse)
def restore_level_subject(
        level_subject_id: UUID,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.restore_academic_level_subject(level_subject_id)


@router.delete("/archive/level-subjects/{level_subject_id}", status_code=204)
def delete_archived_level_subject(
        level_subject_id: UUID,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.delete_archived_academic_level_subject(level_subject_id)




#Active routers
@router.post("/level-subjects/{level_id}", response_model= AcademicLevelSubjectResponse, status_code=201)
def assign_level_subject(
        level_id: UUID,
        payload:AcademicLevelSubjectCreate,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.create_academic_level_subject(level_id, payload)


@router.get("/level-subjects/", response_model=List[AcademicLevelSubjectResponse])
def get_level_subjects(
        filters: AcademicLevelSubjectFilterParams = Depends(),
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.get_all_academic_level_subjects(filters)


@router.get("/level-subjects/{level_subject_id}/audit", response_model=AcademicLevelSubjectAudit)
def get_level_subject_audit(
        level_subject_id: UUID,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.get_academic_level_subject(level_subject_id)



@router.get("/level-subjects/{level_subject_id}", response_model=AcademicLevelSubjectResponse)
def get_level_subject(
        level_subject_id: UUID,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.get_academic_level_subject(level_subject_id)


@router.patch("/level-subjects/{level_subject_id}",  status_code=204)
def archive_level_subject(
        level_subject_id: UUID,
        reason:ArchiveRequest,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.archive_academic_level_subject(level_subject_id, reason.reason)


@router.post("/level-subjects/{level_subject_id}", response_class=FileResponse,  status_code=204)
def export_level_subject_audit(
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


@router.delete("/level-subjects/{level_subject_id}", status_code=204)
def delete_level_subject(
        level_subject_id: UUID,
        factory: AcademicLevelSubjectFactory = Depends(get_authenticated_factory(AcademicLevelSubjectFactory))
    ):
    return factory.delete_academic_level_subject(level_subject_id)










