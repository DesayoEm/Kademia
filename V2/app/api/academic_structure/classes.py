
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter

from V2.app.core.academic_structure.crud.classes import ClassCrud
from V2.app.core.academic_structure.schemas.classes import(
    ClassCreate, ClassUpdate, ClassFilterParams, ClassResponse
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/", response_model= ClassResponse, status_code=201)
def create_class(
        data:ClassCreate,
        crud: ClassCrud = Depends(get_authenticated_crud(ClassCrud))
    ):
    return crud.create_class(data)


@router.get("/", response_model=List[ClassResponse])
def get_classes(
        filters: ClassFilterParams = Depends(),
        crud: ClassCrud = Depends(get_authenticated_crud(ClassCrud))
    ):
    return crud.get_all_classes(filters)


@router.get("/{class_id}", response_model=ClassResponse)
def get_class(
        class_id: UUID,
        crud: ClassCrud = Depends(get_authenticated_crud(ClassCrud))
):
    return crud.get_class(class_id)


@router.put("/{class_id}", response_model=ClassResponse)
def update_class(
        data: ClassUpdate,
        class_id: UUID,
        crud: ClassCrud = Depends(get_authenticated_crud(ClassCrud))
):
    return crud.update_class(class_id, data)


@router.patch("/{class_id}",  status_code=204)
def archive_class(
        class_id: UUID,
        reason:ArchiveRequest,
        crud: ClassCrud = Depends(get_authenticated_crud(ClassCrud))
    ):
    return crud.archive_class(class_id, reason.reason)


@router.post("/{class_id}", response_class=FileResponse,  status_code=204)
def export_class(
        class_id: UUID,
        export_format: ExportFormat,
        crud: ClassCrud = Depends(get_authenticated_crud(ClassCrud))
    ):
    file_path= crud.export_class(class_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{class_id}", status_code=204)
def delete_class(
        class_id: UUID,
        crud: ClassCrud = Depends(get_authenticated_crud(ClassCrud))
    ):
    return crud.delete_class(class_id)










