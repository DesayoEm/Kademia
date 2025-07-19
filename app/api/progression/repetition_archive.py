from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from app.core.progression.factories.repetition import RepetitionFactory
from app.core.progression.schemas.repetition import (
    RepetitonResponse,
    RepetitionFilterParams, 
    RepetitonAudit
)

from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[RepetitonResponse])
def get_all_archived_repetitions(
        filters: RepetitionFilterParams = Depends(), 
        factory: RepetitionFactory = Depends(get_authenticated_factory(RepetitionFactory))
    ):
    return factory.get_all_archived_repetitions(filters)


@router.get("/{repetition_id}/audit", response_model=RepetitonAudit)
def get_archived_repetition_audit(
        repetition_id: UUID,
        factory: RepetitionFactory = Depends(get_authenticated_factory(RepetitionFactory))
    ):
    return factory.get_archived_repetition(repetition_id)


@router.get("/{repetition_id}", response_model=RepetitonResponse)
def get_archived_repetition(
        repetition_id: UUID,
        factory: RepetitionFactory = Depends(get_authenticated_factory(RepetitionFactory))
    ):
    return factory.get_archived_repetition(repetition_id)


@router.patch("/{repetition_id}", response_model=RepetitonResponse)
def restore_repetition(
        repetition_id: UUID,
        factory: RepetitionFactory = Depends(get_authenticated_factory(RepetitionFactory))
    ):
    return factory.restore_repetition(repetition_id)


@router.delete("/{repetition_id}", status_code=204)
def delete_archived_repetition(
        repetition_id: UUID,
        factory: RepetitionFactory = Depends(get_authenticated_factory(RepetitionFactory))
    ):
    return factory.delete_archived_repetition(repetition_id)
