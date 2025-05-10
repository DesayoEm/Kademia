
from uuid import UUID
from V2.app.core.staff_management.crud.qualification import QualificationCrud
from V2.app.core.staff_management.schemas.qualification import QualificationResponse, QualificationFilterParams
from fastapi import Depends, APIRouter
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud, get_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.get("/", response_model=list[QualificationResponse])
def get_archived_qualifications(
        filters: QualificationFilterParams = Depends(),
        crud: QualificationCrud = Depends(get_authenticated_crud(QualificationCrud))
    ):
    return crud.get_all_archived_qualifications(filters)


@router.get("/{qualification_id}", response_model=QualificationResponse)
def get_archived_qualification(
        qualification_id: UUID,
        crud: QualificationCrud = Depends(get_authenticated_crud(QualificationCrud))
    ):
    return crud.get_archived_qualification(qualification_id)


@router.patch("/{qualification_id}", response_model=QualificationResponse)
def restore_qualification(
        qualification_id: UUID,
        crud: QualificationCrud = Depends(get_authenticated_crud(QualificationCrud))
    ):
    return crud.restore_qualification(qualification_id)


@router.delete("/{qualification_id}", status_code=204)
def delete_archived_qualification(
        qualification_id: UUID,
        crud: QualificationCrud = Depends(get_authenticated_crud(QualificationCrud))
    ):
    return crud.delete_archived_qualification(qualification_id)











