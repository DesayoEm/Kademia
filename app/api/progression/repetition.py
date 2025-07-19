from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from app.core.progression.factories.repetition import RepetitionFactory
from app.core.progression.schemas.repetition import (
    RepetitonCreate,
    RepetitonResponse,
    RepetitionFilterParams,
    RepetitonAudit, RepetitonReview, RepetitonDecision
)
from fastapi.responses import FileResponse
from app.core.shared.schemas.enums import ExportFormat
from app.core.progression.services.repetition_service import RepetitionService
from app.core.shared.schemas.shared_models import ArchiveRequest
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("/{student_id}/repetitions", response_model=RepetitonResponse, status_code=201)
def create_repetition(
        student_id: UUID,
        payload: RepetitonCreate,
        factory: RepetitionFactory = Depends(get_authenticated_factory(RepetitionFactory))
    ):
    return factory.create_repetition(student_id, payload)


@router.get("/", response_model=List[RepetitonResponse])
def get_all_repetitions(
        filters: RepetitionFilterParams = Depends(),
        factory: RepetitionFactory = Depends(get_authenticated_factory(RepetitionFactory))
    ):
    return factory.get_all_repetitions(filters)


@router.get("/{repetition_id}/audit", response_model=RepetitonAudit)
def get_repetition_audit(
        repetition_id: UUID,
        factory: RepetitionFactory = Depends(get_authenticated_factory(RepetitionFactory))
    ):
    return factory.get_repetition(repetition_id)


@router.patch("/{student_id}/repetitions/action", response_model=RepetitonResponse)
def action_repetition(
        repetition_id: UUID,
        payload: RepetitonDecision,
        service: RepetitionService = Depends(get_authenticated_factory(RepetitionService))
    ):
    payload = payload.model_dump(exclude_unset=True)
    return service.action_repetition_record(repetition_id, payload)


@router.patch("/{student_id}/repetitions", response_model=RepetitonResponse)
def update_repetition(
        repetition_id: UUID,
        payload: RepetitonReview,
        factory: RepetitionFactory = Depends(get_authenticated_factory(RepetitionFactory))
    ):
    payload = payload.model_dump(exclude_unset=True)
    return factory.update_repetition(repetition_id, payload)


@router.get("/{repetition_id}", response_model=RepetitonResponse)
def get_repetition(
        repetition_id: UUID,
        factory: RepetitionFactory = Depends(get_authenticated_factory(RepetitionFactory))
    ):
    return factory.get_repetition(repetition_id)


@router.patch("/{repetition_id}", status_code=204)
def archive_repetition(
        repetition_id: UUID,
        reason: ArchiveRequest,
        factory: RepetitionFactory = Depends(get_authenticated_factory(RepetitionFactory))
    ):
    return factory.archive_repetition(repetition_id, reason.reason)


@router.delete("/{repetition_id}", status_code=204)
def delete_repetition(
        repetition_id: UUID,
        factory: RepetitionFactory = Depends(get_authenticated_factory(RepetitionFactory))
    ):
    return factory.delete_repetition(repetition_id)


@router.post("/{repetition_id}", response_class=FileResponse,  status_code=204)
def export_repetition_audit(
        repetition_id: UUID,
        export_format: ExportFormat,
        service: RepetitionService = Depends(get_authenticated_service(RepetitionService)),
    ):
    file_path= service.export_repetition_audit(repetition_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

