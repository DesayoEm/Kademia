from fastapi import APIRouter, Depends

from uuid import UUID
from typing import List

from V2.app.core.progression.factories.promotion import PromotionFactory

from V2.app.core.progression.schemas.promotion import (
    PromotionCreate,
    PromotionResponse,
    PromotionFilterParams,
    PromotionAudit
)
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

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
