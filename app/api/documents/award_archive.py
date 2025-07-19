
from typing import List
from uuid import UUID
from fastapi import Depends, APIRouter
from app.core.documents.schemas.student_award import AwardFilterParams, AwardResponse, AwardAudit
from app.core.documents.factories.award_factory import AwardFactory
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[AwardResponse])
def get_archived_awards(
        filters: AwardFilterParams = Depends(),
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.get_all_archived_awards(filters)


@router.get("/{award_id}/audit", response_model=AwardAudit)
def get_archived_award_audit(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.get_archived_award(award_id)


@router.get("/{award_id}", response_model=AwardResponse)
def get_archived_award(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.get_archived_award(award_id)


@router.patch("/{award_id}", response_model=AwardResponse)
def restore_award(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.restore_award(award_id)


@router.delete("/{award_id}", status_code=204)
def delete_archived_award(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.delete_archived_award(award_id)




