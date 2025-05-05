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

router = APIRouter()


@router.get("/", response_model=List[StudentPromotionResponse])
def get_all_archived_promotions(filters: PromotionFilterParams = Depends(), db: Session = Depends(get_db)):
    crud = PromotionCrud(db)
    return crud.get_all_archived_promotions(filters)


@router.get("/{promotion_id}", response_model=StudentPromotionResponse)
def get_archived_promotion(promotion_id: UUID, db: Session = Depends(get_db)):
    crud = PromotionCrud(db)
    return crud.get_archived_promotion(promotion_id)


@router.patch("/{promotion_id}", response_model=StudentPromotionResponse)
def restore_promotion(promotion_id: UUID, db: Session = Depends(get_db)):
    crud = PromotionCrud(db)
    return crud.restore_promotion(promotion_id)


@router.delete("/{promotion_id}", status_code=204)
def delete_archived_promotion(promotion_id: UUID, db: Session = Depends(get_db)):
    crud = PromotionCrud(db)
    return crud.delete_archived_promotion(promotion_id)
