from uuid import UUID
from typing import List
from fastapi.responses import FileResponse
from fastapi import Depends, APIRouter
from app.core.shared.schemas.enums import ExportFormat
from app.core.shared.schemas.shared_models import ArchiveRequest
from app.core.staff_management.factories.department import StaffDepartmentFactory
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service

from app.core.staff_management.schemas.department import (
    StaffDepartmentCreate, StaffDepartmentUpdate, StaffDepartmentResponse,
    DepartmentFilterParams, StaffDepartmentAudit
)
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.staff_management.services.staff_management import StaffManagementService

token_service = TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/", response_model=StaffDepartmentResponse, status_code=201)
def create_staff_department(
        payload: StaffDepartmentCreate,
        factory: StaffDepartmentFactory = Depends(get_authenticated_factory(StaffDepartmentFactory))
    ):
    """Create a new staff department."""

    return factory.create_staff_department(payload)


@router.get("/", response_model=List[StaffDepartmentResponse])
def get_all_departments(
        filters: DepartmentFilterParams = Depends(),
        factory: StaffDepartmentFactory = Depends(get_authenticated_factory(StaffDepartmentFactory))
    ):
    """Get all active departments."""
    return factory.get_all_departments(filters)


@router.get("/{department_id}/audit", response_model=StaffDepartmentAudit)
def get_staff_department_audit(
        department_id: UUID,
        factory: StaffDepartmentFactory = Depends(get_authenticated_factory(StaffDepartmentFactory))
    ):
    """Get a department audit by ID."""
    return factory.get_staff_department(department_id)


@router.get("/{department_id}", response_model=StaffDepartmentResponse)
def get_staff_department(
        department_id: UUID,
        factory: StaffDepartmentFactory = Depends(get_authenticated_factory(StaffDepartmentFactory))
    ):
    """Get a specific department by ID."""

    return factory.get_staff_department(department_id)


@router.put("/{department_id}/manager", response_model=StaffDepartmentResponse)
def assign_department_manager(
        department_id: UUID,
        manager_id: UUID,
        service: StaffManagementService = Depends(get_authenticated_service(StaffManagementService))
    ):
    """Assign a manager to a department."""
    return service.assign_manager(department_id, manager_id)


@router.put("/{department_id}/manager/remove", response_model=StaffDepartmentResponse)
def remove_department_manager(
        department_id: UUID,
        service: StaffManagementService = Depends(get_authenticated_service(StaffManagementService))
    ):
    """Remove manager from a department."""
    return service.assign_manager(department_id)


@router.put("/{department_id}", response_model=StaffDepartmentResponse)
def update_staff_department(
        department_id: UUID,
        payload: StaffDepartmentUpdate,
        factory: StaffDepartmentFactory = Depends(get_authenticated_factory(StaffDepartmentFactory))
    ):
    """Update a staff department."""
    update_data = payload.model_dump(exclude_unset=True)
    return factory.update_staff_department(department_id, update_data)


@router.post("/{department_id}/export", response_class=FileResponse)
def export_department(
        department_id: UUID,
        export_format: ExportFormat,
        service: StaffManagementService = Depends(get_authenticated_service(StaffManagementService))
):
    """Export department data."""
    file_path = service.export_department(department_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.patch("/{department_id}/archive", status_code=204)
def archive_department(
        department_id: UUID,
        reason: ArchiveRequest,
        factory: StaffDepartmentFactory = Depends(get_authenticated_factory(StaffDepartmentFactory))
    ):
    """Archive a department."""
    return factory.archive_department(department_id, reason.reason)


@router.delete("/{department_id}", status_code=204)
def delete_department(
        department_id: UUID,
        factory: StaffDepartmentFactory = Depends(get_authenticated_factory(StaffDepartmentFactory))
    ):
    """Delete a department permanently."""
    return factory.delete_department(department_id)