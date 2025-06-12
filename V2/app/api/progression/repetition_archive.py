from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.infra.db.session_manager import get_db
from V2.app.core.progression.crud.repetition import RepetitionCrud
from V2.app.core.progression.schemas.repetition import (
    StudentRepetitionResponse,
    RepetitionFilterParams
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[StudentRepetitionResponse])
def get_all_archived_repetitions(
        filters: RepetitionFilterParams = Depends(), 
        crud: RepetitionCrud = Depends(get_authenticated_crud(RepetitionCrud))
    ):
    return crud.get_all_archived_repetitions(filters)


@router.get("/{repetition_id}", response_model=StudentRepetitionResponse)
def get_archived_repetition(
        repetition_id: UUID,
        crud: RepetitionCrud = Depends(get_authenticated_crud(RepetitionCrud))
    ):
    return crud.get_archived_repetition(repetition_id)


@router.patch("/{repetition_id}", response_model=StudentRepetitionResponse)
def restore_repetition(
        repetition_id: UUID,
        crud: RepetitionCrud = Depends(get_authenticated_crud(RepetitionCrud))
    ):
    return crud.restore_repetition(repetition_id)


@router.delete("/{repetition_id}", status_code=204)
def delete_archived_repetition(
        repetition_id: UUID,
        crud: RepetitionCrud = Depends(get_authenticated_crud(RepetitionCrud))
    ):
    return crud.delete_archived_repetition(repetition_id)
