from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.infra.db.session_manager import get_db
from V2.app.core.progression.crud.graduation import GraduationCrud
from V2.app.core.progression.schemas.graduation import (
    GraduationResponse,
    GraduationFilterParams
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[GraduationResponse])
def get_all_archived_graduations(
        filters: GraduationFilterParams = Depends(),
        crud: GraduationCrud = Depends(get_authenticated_crud(GraduationCrud))
    ):
    return crud.get_all_archived_graduations(filters)


@router.get("/{graduation_id}", response_model=GraduationResponse)
def get_archived_graduation(
        graduation_id: UUID,
        crud: GraduationCrud = Depends(get_authenticated_crud(GraduationCrud))
    ):
    return crud.get_archived_graduation(graduation_id)


@router.patch("/{graduation_id}", response_model=GraduationResponse)
def restore_graduation(
        graduation_id: UUID,
        crud: GraduationCrud = Depends(get_authenticated_crud(GraduationCrud))
    ):
    return crud.restore_graduation(graduation_id)


@router.delete("/{graduation_id}", status_code=204)
def delete_archived_graduation(
        graduation_id: UUID,
        crud: GraduationCrud = Depends(get_authenticated_crud(GraduationCrud))
    ):
    return crud.delete_archived_graduation(graduation_id)
