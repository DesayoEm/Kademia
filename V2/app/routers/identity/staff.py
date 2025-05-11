
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.identity.schemas.staff import StaffCreate, StaffUpdate, StaffResponse, StaffFilterParams
from fastapi import Depends, APIRouter
from V2.app.core.identity.crud.staff import StaffCrud
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/", response_model= StaffResponse, status_code=201)
def create_staff(
        data:StaffCreate,
        crud: StaffCrud = Depends(get_authenticated_crud(StaffCrud)),
    ):
        return crud.create_staff(data)


@router.get("/", response_model=List[StaffResponse])
def get_staff(
        filters: StaffFilterParams = Depends(),
        crud: StaffCrud = Depends(get_authenticated_crud(StaffCrud))
    ):
        return crud.get_all_staff(filters)


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(
        staff_id: UUID,
        crud: StaffCrud = Depends(get_authenticated_crud(StaffCrud))
    ):
        return crud.get_staff(staff_id)


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(
        data: StaffUpdate,
        staff_id: UUID,
        crud: StaffCrud = Depends(get_authenticated_crud(StaffCrud))
    ):
        return crud.update_staff(staff_id, data)


@router.patch("/{staff_id}", status_code=204)
def archive_staff(
        staff_id: UUID,
        reason:ArchiveRequest,
        crud: StaffCrud = Depends(get_authenticated_crud(StaffCrud))
    ):
        return crud.archive_staff(staff_id, reason.reason)


@router.post("/{staff_id}", response_class=FileResponse,  status_code=204)
def export_staff(
        staff_id: UUID,
        export_format: ExportFormat,
        crud: StaffCrud = Depends(get_authenticated_crud(StaffCrud))
    ):
    file_path= crud.export_staff(staff_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{staff_id}", status_code=204)
def delete_staff(
        staff_id: UUID,
        crud: StaffCrud = Depends(get_authenticated_crud(StaffCrud))
    ):
        return crud.delete_staff(staff_id)











