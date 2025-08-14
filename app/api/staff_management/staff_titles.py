from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter

from app.core.shared.schemas.shared_models import ArchiveRequest
from app.core.staff_management.factories.staff_title import StaffTitleFactory
from app.core.staff_management.schemas.staff_title import (
    StaffTitleCreate, StaffTitleUpdate, StaffTitleFilterParams, StaffTitleResponse, StaffTitleAudit
)
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer


token_service = TokenService()
access = AccessTokenBearer()
router = APIRouter()


#Archive routers
@router.get("/archive/titles/", response_model=List[StaffTitleResponse])
def get_archived_titles(
        filters: StaffTitleFilterParams = Depends(),
        factory: StaffTitleFactory = Depends(get_authenticated_factory(StaffTitleFactory))
    ):
    return factory.get_all_archived_titles(filters)


@router.get("/archive/titles/{title_id}/audit", response_model=StaffTitleAudit)
def get_archived_staff_title_audit(
        title_id: UUID,
        factory: StaffTitleFactory = Depends(get_authenticated_factory(StaffTitleFactory))
    ):
    """Get an archived title audit by ID."""
    return factory.get_archived_title(title_id)


@router.get("/archive/titles/{title_id}", response_model=StaffTitleResponse)
def get_archived_title(
        title_id: UUID,
        factory: StaffTitleFactory = Depends(get_authenticated_factory(StaffTitleFactory))
    ):
    return factory.get_archived_title(title_id)


@router.patch("/archive/titles/{title_id}", response_model=StaffTitleResponse)
def restore_title(
        title_id: UUID,
        factory: StaffTitleFactory = Depends(get_authenticated_factory(StaffTitleFactory))
    ):
    return factory.restore_title(title_id)


@router.delete("/archive/titles/{title_id}", status_code=204)
def delete_archived_title(
        title_id: UUID,
        factory: StaffTitleFactory = Depends(get_authenticated_factory(StaffTitleFactory))
    ):
    return factory.delete_archived_title(title_id)


#Active routers

@router.post("/titles", response_model= StaffTitleResponse, status_code = 201)
def create_title(
        payload:StaffTitleCreate,
        factory: StaffTitleFactory = Depends(get_authenticated_factory(StaffTitleFactory))
    ):
        return factory.create_title(payload)


@router.get("/titles/", response_model= List[StaffTitleResponse])
def get_titles(
        filters: StaffTitleFilterParams = Depends(),
        factory: StaffTitleFactory = Depends(get_authenticated_factory(StaffTitleFactory))
    ):
        return factory.get_all_titles(filters)


@router.get("/titles/{title_id}/audit", response_model=StaffTitleAudit)
def get_staff_title_audit(
        title_id: UUID,
        factory: StaffTitleFactory = Depends(get_authenticated_factory(StaffTitleFactory))
    ):
    """Get a title audit by ID."""
    return factory.get_title(title_id)


@router.get("/titles/{title_id}", response_model=StaffTitleResponse)
def get_title(
        title_id: UUID,
        factory: StaffTitleFactory = Depends(get_authenticated_factory(StaffTitleFactory))
    ):
        return factory.get_title(title_id)


@router.put("/titles/{title_id}", response_model=StaffTitleResponse)
def update_title(
        payload: StaffTitleUpdate,
        title_id: UUID,
        factory: StaffTitleFactory = Depends(get_authenticated_factory(StaffTitleFactory))
    ):
        update_data = payload.model_dump(exclude_unset=True)
        return factory.update_title(title_id, update_data)


@router.patch("/titles/{title_id}", status_code=204)
def archive_title(
        title_id: UUID,
        reason:ArchiveRequest,
        factory: StaffTitleFactory = Depends(get_authenticated_factory(StaffTitleFactory))
    ):
        return factory.archive_title(title_id, reason.reason)



@router.delete("/{title_id}", status_code=204)
def delete_title(
        title_id: UUID,
        factory: StaffTitleFactory = Depends(get_authenticated_factory(StaffTitleFactory))
    ):
        return factory.delete_title(title_id)


