
from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from V2.app.core.identity.schemas.guardian import GuardianResponse, GuardianFilterParams, GuardianAudit
from V2.app.core.identity.factories.guardian import GuardianFactory
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory 

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[GuardianResponse])
def get_archived_guardians(
        filters: GuardianFilterParams = Depends(),
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
    return factory.get_all_archived_guardians(filters)


@router.get("/{guardian_id}/audit", response_model=GuardianAudit)
def get_archived_guardian_audit(
        guardian_id: UUID,
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
    return factory.get_archived_guardian(guardian_id)

@router.get("/{guardian_id}", response_model=GuardianResponse)
def get_archived_guardian(
        guardian_id: UUID,
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
    return factory.get_archived_guardian(guardian_id)


@router.patch("/{guardian_id}", response_model=GuardianResponse)
def restore_guardian(
        guardian_id: UUID,
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
    return factory.restore_guardian(guardian_id)


@router.delete("/{guardian_id}", status_code=204)
def delete_archived_guardian(
        guardian_id: UUID,
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
    return factory.delete_archived_guardian(guardian_id)











