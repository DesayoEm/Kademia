
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.documents.factories.award_factory import AwardFactory
from V2.app.core.documents.services.document_service import DocumentService
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.core.documents.schemas.student_award import (
    AwardFilterParams, AwardCreate, AwardUpdate, AwardResponse, AwardAudit
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("{student_id}/", response_model= AwardResponse, status_code=201)
def create_award(
        student_id: UUID,
        payload:AwardCreate,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.create_award(student_id, payload)


@router.get("/", response_model=List[AwardResponse])
def get_awards(
        filters: AwardFilterParams = Depends(),
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.get_all_awards(filters)


@router.get("/{award_id}/audit", response_model=AwardAudit)
def get_award_audit(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
     ):
    return factory.get_award(award_id)


@router.get("/{award_id}", response_model=AwardResponse)
def get_award(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
     ):
    return factory.get_award(award_id)


@router.put("/{award_id}", response_model=AwardResponse)
def update_award(
        payload: AwardUpdate,
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    payload = payload.model_dump(exclude_unset=True)
    return factory.update_award(award_id, payload)


@router.patch("/{award_id}",  status_code=204)
def archive_award(
        award_id: UUID,
        reason:ArchiveRequest,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.archive_award(award_id, reason.reason)


@router.post("/{award_id}/audit", response_class=FileResponse,  status_code=204)
def export_award_audit(
        award_id: UUID,
        export_format: ExportFormat,
        service: DocumentService = Depends(get_authenticated_service(DocumentService))
):
    file_path= service.export_award_audit(award_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{award_id}", status_code=204)
def delete_award(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
):
    return factory.delete_award(award_id)










