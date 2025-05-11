from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter

from V2.app.core.identity.schemas.guardian import GuardianResponse, GuardianFilterParams
from V2.app.core.identity.crud.guardian import GuardianCrud
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=List[GuardianResponse])
def get_archived_guardians(
        filters: GuardianFilterParams = Depends(),
        crud: GuardianCrud = Depends(get_authenticated_crud(GuardianCrud))
    ):
    return crud.get_all_archived_guardians(filters)


@router.get("/{guardian_id}", response_model=GuardianResponse)
def get_archived_guardian(
        guardian_id: UUID,
        crud: GuardianCrud = Depends(get_authenticated_crud(GuardianCrud))
    ):
    return crud.get_archived_guardian(guardian_id)


@router.patch("/{guardian_id}", response_model=GuardianResponse)
def restore_guardian(
        guardian_id: UUID,
        crud: GuardianCrud = Depends(get_authenticated_crud(GuardianCrud))
    ):
    return crud.restore_guardian(guardian_id)


@router.delete("/{guardian_id}", status_code=204)
def delete_archived_guardian(
        guardian_id: UUID,
        crud: GuardianCrud = Depends(get_authenticated_crud(GuardianCrud))
    ):
    return crud.delete_archived_guardian(guardian_id)











