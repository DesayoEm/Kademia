
from uuid import UUID
from typing import List

from V2.app.core.academic_structure.schemas.classes import ClassFilterParams, ClassResponse, ClassAudit
from fastapi import Depends, APIRouter
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory

from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.academic_structure.factories.classes import ClassFactory


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.get("/", response_model=List[ClassResponse])
def get_archived_classes(
        filters: ClassFilterParams = Depends(),
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
    ):
    return factory.get_all_archived_classes(filters)


@router.get("/{class_id}/audit", response_model=ClassAudit)
def get_archived_class_audit(
        class_id: UUID,
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
    ):
    return factory.get_archived_class(class_id)


@router.get("/{class_id}", response_model=ClassResponse)
def get_archived_class(
        class_id: UUID,
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
    ):
    return factory.get_archived_class(class_id)


@router.patch("/{class_id}", response_model=ClassResponse)
def restore_class(
        class_id: UUID,
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
    ):
    return factory.restore_class(class_id)


@router.delete("/{class_id}", status_code=204)
def delete_archived_class(
        class_id: UUID,
        factory: ClassFactory = Depends(get_authenticated_factory(ClassFactory))
    ):
    return factory.delete_archived_class(class_id)




