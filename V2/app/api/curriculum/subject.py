from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.curriculum.factories.subject import SubjectFactory
from V2.app.core.curriculum.services.curriculum_service import CurriculumService
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter

from V2.app.core.curriculum.schemas.subject import (
    SubjectCreate, SubjectUpdate, SubjectFilterParams, SubjectResponse, SubjectAudit
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("/", response_model= SubjectResponse, status_code=201)
def create_subject(
        payload:SubjectCreate,
        factory: SubjectFactory = Depends(get_authenticated_factory(SubjectFactory))
    ):
    return factory.create_subject(payload)


@router.get("/", response_model=List[SubjectResponse])
def get_subjects(
        filters: SubjectFilterParams = Depends(),
        factory: SubjectFactory = Depends(get_authenticated_factory(SubjectFactory))
    ):
    return factory.get_all_subjects(filters)


@router.get("/{subject_id}/audit", response_model=SubjectAudit)
def get_subject_audit(
        subject_id: UUID,
        factory: SubjectFactory = Depends(get_authenticated_factory(SubjectFactory))
    ):
    return factory.get_subject(subject_id)


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(
        subject_id: UUID,
        factory: SubjectFactory = Depends(get_authenticated_factory(SubjectFactory))
    ):
    return factory.get_subject(subject_id)


@router.post("/{subject_id}/audit", response_class=FileResponse, status_code=204)
def export_subject_audit(
        subject_id: UUID,
        export_format: ExportFormat,
        service: CurriculumService = Depends(get_authenticated_service(CurriculumService))
):
    file_path = service.export_subject_audit(subject_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )



@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
        payload: SubjectUpdate,
        subject_id: UUID,
        factory: SubjectFactory = Depends(get_authenticated_factory(SubjectFactory))
    ):
    payload = payload.model_dump(exclude_unset=True)
    return factory.update_subject(subject_id, payload)


@router.patch("/{subject_id}",  status_code=204)
def archive_subject(
        subject_id: UUID,
        reason:ArchiveRequest,
        factory: SubjectFactory = Depends(get_authenticated_factory(SubjectFactory))
    ):
    return factory.archive_subject(subject_id, reason.reason)


@router.delete("/{subject_id}", status_code=204)
def delete_subject(
        subject_id: UUID,
        factory: SubjectFactory = Depends(get_authenticated_factory(SubjectFactory))
    ):
    return factory.delete_subject(subject_id)










