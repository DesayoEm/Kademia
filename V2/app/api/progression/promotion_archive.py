from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List

from V2.app.core.progression.factories.promotion import PromotionFactory
from V2.app.core.progression.schemas.promotion import (
    PromotionResponse,
    PromotionFilterParams, PromotionAudit
)

from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[PromotionResponse])
def get_all_archived_promotions(
        filters: PromotionFilterParams = Depends(),
        factory: PromotionFactory = Depends(get_authenticated_factory(PromotionFactory))
    ):
    return factory.get_all_archived_promotions(filters)


@router.get("/{promotion_id}/audit", response_model=PromotionAudit)
def get_archived_promotion_audit(
        promotion_id: UUID,
        factory: PromotionFactory = Depends(get_authenticated_factory(PromotionFactory))
    ):
    return factory.get_archived_promotion(promotion_id)


@router.get("/{promotion_id}", response_model=PromotionResponse)
def get_archived_promotion(
        promotion_id: UUID,
        factory: PromotionFactory = Depends(get_authenticated_factory(PromotionFactory))
    ):
    return factory.get_archived_promotion(promotion_id)


@router.patch("/{promotion_id}", response_model=PromotionResponse)
def restore_promotion(
        promotion_id: UUID,
        factory: PromotionFactory = Depends(get_authenticated_factory(PromotionFactory))
    ):
    return factory.restore_promotion(promotion_id)


@router.delete("/{promotion_id}", status_code=204)
def delete_archived_promotion(
        promotion_id: UUID,
        factory: PromotionFactory = Depends(get_authenticated_factory(PromotionFactory))
    ):
    return factory.delete_archived_promotion(promotion_id)
