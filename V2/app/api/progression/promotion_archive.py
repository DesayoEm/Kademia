from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.infra.db.session_manager import get_db
from V2.app.core.progression.crud.promotion import PromotionCrud
from V2.app.core.progression.schemas.promotion import (
    StudentPromotionResponse,
    PromotionFilterParams
)
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[StudentPromotionResponse])
def get_all_archived_promotions(
        filters: PromotionFilterParams = Depends(),
        crud: PromotionCrud = Depends(get_authenticated_crud(PromotionCrud))
    ):
    return crud.get_all_archived_promotions(filters)


@router.get("/{promotion_id}", response_model=StudentPromotionResponse)
def get_archived_promotion(
        promotion_id: UUID,
        crud: PromotionCrud = Depends(get_authenticated_crud(PromotionCrud))
    ):
    return crud.get_archived_promotion(promotion_id)


@router.patch("/{promotion_id}", response_model=StudentPromotionResponse)
def restore_promotion(
        promotion_id: UUID,
        crud: PromotionCrud = Depends(get_authenticated_crud(PromotionCrud))
    ):
    return crud.restore_promotion(promotion_id)


@router.delete("/{promotion_id}", status_code=204)
def delete_archived_promotion(
        promotion_id: UUID,
        crud: PromotionCrud = Depends(get_authenticated_crud(PromotionCrud))
    ):
    return crud.delete_archived_promotion(promotion_id)
