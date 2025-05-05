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

router = APIRouter()


@router.post("/students/{student_id}", response_model=StudentPromotionResponse, status_code=201)
def create_promotion(student_id: UUID, data: StudentPromotionCreate, db: Session = Depends(get_db)):
    crud = PromotionCrud(db)
    return crud.create_promotion(student_id, data)


@router.get("/", response_model=List[StudentPromotionResponse])
def get_all_promotions(filters: PromotionFilterParams = Depends(), db: Session = Depends(get_db)):
    crud = PromotionCrud(db)
    return crud.get_all_promotions(filters)


@router.get("/{promotion_id}", response_model=StudentPromotionResponse)
def get_promotion(promotion_id: UUID, db: Session = Depends(get_db)):
    crud = PromotionCrud(db)
    return crud.get_promotion(promotion_id)


@router.put("/{promotion_id}", response_model=StudentPromotionResponse)
def update_promotion(promotion_id: UUID, data: StudentPromotionCreate, db: Session = Depends(get_db)):
    crud = PromotionCrud(db)
    return crud.update_promotion(promotion_id, data)


@router.patch("/{promotion_id}", status_code=204)
def archive_promotion(promotion_id: UUID, reason: ArchiveRequest, db: Session = Depends(get_db)):
    crud = PromotionCrud(db)
    return crud.archive_promotion(promotion_id, reason.reason)


@router.delete("/{promotion_id}", status_code=204)
def delete_promotion(promotion_id: UUID, db: Session = Depends(get_db)):
    crud = PromotionCrud(db)
    return crud.delete_promotion(promotion_id)
