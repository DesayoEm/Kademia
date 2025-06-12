from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.infra.db.session_manager import get_db
from V2.app.core.progression.crud.promotion import PromotionCrud
from V2.app.core.progression.schemas.promotion import (
    StudentPromotionCreate,
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



@router.post("/students/{student_id}", response_model=StudentPromotionResponse, status_code=201)
def create_promotion(
        student_id: UUID, 
        payload: StudentPromotionCreate, 
        crud: PromotionCrud = Depends(get_authenticated_crud(PromotionCrud))
    ):
    return crud.create_promotion(student_id, payload)


@router.get("/", response_model=List[StudentPromotionResponse])
def get_all_promotions(
        filters: PromotionFilterParams = Depends(),
        crud: PromotionCrud = Depends(get_authenticated_crud(PromotionCrud))
    ):
    return crud.get_all_promotions(filters)


@router.get("/{promotion_id}", response_model=StudentPromotionResponse)
def get_promotion(
        promotion_id: UUID,
        crud: PromotionCrud = Depends(get_authenticated_crud(PromotionCrud))
    ):
    return crud.get_promotion(promotion_id)


@router.patch("/{promotion_id}", status_code=204)
def archive_promotion(
        promotion_id: UUID,
        reason: ArchiveRequest,
        crud: PromotionCrud = Depends(get_authenticated_crud(PromotionCrud))
    ):
    return crud.archive_promotion(promotion_id, reason.reason)


@router.delete("/{promotion_id}", status_code=204)
def delete_promotion(
        promotion_id: UUID,
        crud: PromotionCrud = Depends(get_authenticated_crud(PromotionCrud))
    ):
    return crud.delete_promotion(promotion_id)
