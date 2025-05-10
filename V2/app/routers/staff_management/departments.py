
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from fastapi import Depends, APIRouter
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from V2.app.core.staff_management.crud.department import StaffDepartmentCrud
from V2.app.core.staff_management.schemas.department import(
    StaffDepartmentCreate, StaffDepartmentUpdate, StaffDepartmentResponse, DepartmentFilterParams
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/", response_model= StaffDepartmentResponse, status_code=201)
def create_staff_department(
        payload:StaffDepartmentCreate,
        crud: StaffDepartmentCrud = Depends(get_authenticated_crud(StaffDepartmentCrud))
):
        return crud.create_department(payload)


@router.get("/", response_model=List[StaffDepartmentResponse])
def get_staff_departments(
        filters: DepartmentFilterParams = Depends(),
        crud: StaffDepartmentCrud = Depends(get_authenticated_crud(StaffDepartmentCrud))
):
        return crud.get_all_departments(filters)


@router.get("/{department_id}", response_model=StaffDepartmentResponse)
def get_staff_department(
        department_id: UUID,
        crud: StaffDepartmentCrud = Depends(get_authenticated_crud(StaffDepartmentCrud))
):
        return crud.get_department(department_id)


@router.put("/{department_id}", response_model=StaffDepartmentResponse)
def update_staff_department(
        payload: StaffDepartmentUpdate,
        department_id: UUID,
        crud: StaffDepartmentCrud = Depends(get_authenticated_crud(StaffDepartmentCrud))
    ):
        return crud.update_department(department_id, payload)


@router.patch("/{department_id}",  status_code=204)
def archive_department(
        department_id: UUID,
        reason:ArchiveRequest,
        crud: StaffDepartmentCrud = Depends(get_authenticated_crud(StaffDepartmentCrud))
    ):
        return crud.archive_department(department_id, reason.reason)


@router.post("/{department_id}", response_class=FileResponse,  status_code=204)
def export_department(
        department_id: UUID,
        export_format: ExportFormat,
        crud: StaffDepartmentCrud = Depends(get_authenticated_crud(StaffDepartmentCrud))
    ):
    file_path= crud.export_department(department_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{department_id}", status_code=204)
def delete_department(
        department_id: UUID,
        crud: StaffDepartmentCrud = Depends(get_authenticated_crud(StaffDepartmentCrud))
    ):
        return crud.delete_department(department_id)










