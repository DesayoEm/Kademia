from fastapi import APIRouter, Depends

from uuid import UUID
from typing import List

from app.core.progression.factories.promotion import PromotionFactory

from app.core.progression.schemas.promotion import (
    PromotionCreate,
    PromotionResponse,
    PromotionFilterParams,
    PromotionAudit, PromotionReview, PromotionDecision
)
from app.core.progression.services.promotion_service import PromotionService
from app.core.shared.schemas.shared_models import ArchiveRequest
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("/students/{student_id}", response_model=PromotionResponse, status_code=201)
def create_promotion(
        student_id: UUID, 
        payload: PromotionCreate, 
        factory: PromotionFactory = Depends(get_authenticated_factory(PromotionFactory))
    ):
    return factory.create_promotion(student_id, payload)


@router.get("/", response_model=List[PromotionResponse])
def get_all_promotions(
        filters: PromotionFilterParams = Depends(),
        factory: PromotionFactory = Depends(get_authenticated_factory(PromotionFactory))
    ):
    return factory.get_all_promotions(filters)


@router.get("/{promotion_id}/audit", response_model=PromotionAudit)
def get_promotion_audit(
        promotion_id: UUID,
        factory: PromotionFactory = Depends(get_authenticated_factory(PromotionFactory))
    ):
    return factory.get_promotion(promotion_id)


@router.get("/{promotion_id}", response_model=PromotionResponse)
def get_promotion(
        promotion_id: UUID,
        factory: PromotionFactory = Depends(get_authenticated_factory(PromotionFactory))
    ):
    return factory.get_promotion(promotion_id)


@router.patch("/{student_id}/promotions/action", response_model=PromotionResponse)
def action_promotion(
        promotion_id: UUID,
        payload: PromotionDecision,
        service: PromotionService = Depends(get_authenticated_service(PromotionService))
    ):
    payload = payload.model_dump(exclude_unset=True)
    return service.action_promotion_record(promotion_id, payload)


@router.patch("/{student_id}/promotions", response_model=PromotionResponse)
def update_promotion(
        promotion_id: UUID,
        payload: PromotionReview,
        factory: PromotionFactory = Depends(get_authenticated_factory(PromotionFactory))
    ):
    payload = payload.model_dump(exclude_unset=True)
    return factory.update_promotion(promotion_id, payload)


@router.patch("/{promotion_id}", status_code=204)
def archive_promotion(
        promotion_id: UUID,
        reason: ArchiveRequest,
        factory: PromotionFactory = Depends(get_authenticated_factory(PromotionFactory))
    ):
    return factory.archive_promotion(promotion_id, reason.reason)


@router.delete("/{promotion_id}", status_code=204)
def delete_promotion(
        promotion_id: UUID,
        factory: PromotionFactory = Depends(get_authenticated_factory(PromotionFactory))
    ):
    return factory.delete_promotion(promotion_id)
