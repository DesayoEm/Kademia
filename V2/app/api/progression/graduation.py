from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from V2.app.infra.db.session_manager import get_db
from V2.app.core.progression.crud.graduation import GraduationCrud
from V2.app.core.progression.schemas.graduation import (
    GraduationCreate,
    GraduationResponse,
    GraduationFilterParams
)
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/students/{student_id}", response_model=GraduationResponse, status_code=201)
def graduate_student(
        student_id: UUID,
        payload: GraduationCreate,
        crud: GraduationCrud = Depends(get_authenticated_crud(GraduationCrud))
    ):
    return crud.create_graduation(student_id, payload)


@router.get("/", response_model=List[GraduationResponse])
def get_all_graduations(
        filters: GraduationFilterParams = Depends(),
        crud: GraduationCrud = Depends(get_authenticated_crud(GraduationCrud))
    ):
    return crud.get_all_graduations(filters)


@router.get("/{graduation_id}", response_model=GraduationResponse)
def get_graduation(
        graduation_id: UUID,
        crud: GraduationCrud = Depends(get_authenticated_crud(GraduationCrud))
    ):
    return crud.get_graduation(graduation_id)


@router.patch("/{graduation_id}", status_code=204)
def archive_graduation(
        graduation_id: UUID,
        reason: ArchiveRequest,
        crud: GraduationCrud = Depends(get_authenticated_crud(GraduationCrud))
    ):
    return crud.archive_graduation(graduation_id, reason.reason)


@router.delete("/{graduation_id}", status_code=204)
def delete_graduation(
        graduation_id: UUID,
        crud: GraduationCrud = Depends(get_authenticated_crud(GraduationCrud))
    ):
    return crud.delete_graduation(graduation_id)
