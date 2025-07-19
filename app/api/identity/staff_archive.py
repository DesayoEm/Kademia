
from uuid import UUID
from typing import List

from app.core.identity.factories.staff import StaffFactory
from app.core.identity.schemas.staff import StaffResponse, StaffFilterParams, StaffAudit
from fastapi import Depends, APIRouter

from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[StaffResponse])
def get_archived_staff(
        filters: StaffFilterParams = Depends(),
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory))
    ):
    return factory.get_all_archived_staff(filters)


@router.get("/{staff_id}/audit", response_model=StaffAudit)
def get_archived_staff_audit(
        staff_id: UUID,
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory))
    ):
    return factory.get_archived_staff(staff_id)


@router.get("/{staff_id}", response_model=StaffResponse)
def get_archived_staff(
        staff_id: UUID,
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory))
    ):
    return factory.get_archived_staff(staff_id)


@router.patch("/{staff_id}", response_model=StaffResponse)
def restore_staff(
        staff_id: UUID,
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory))
    ):
    return factory.restore_staff(staff_id)


@router.delete("/{staff_id}", status_code=204)
def delete_archived_staff(
        staff_id: UUID,
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory))
    ):
    return factory.delete_archived_staff(staff_id)











