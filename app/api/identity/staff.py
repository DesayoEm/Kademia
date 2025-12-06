from uuid import UUID
from typing import List
from fastapi.responses import FileResponse
from fastapi import UploadFile, File

from app.core.rbac.factories.role_history import RoleHistoryFactory
from app.core.rbac.schemas.role_history import (
    RoleHistoryCreate,
    RoleHistoryResponse,
    RoleHistoryFilterParams,
)
from app.core.identity.factories.staff import StaffFactory
from app.core.identity.services.profile_picture_service import ProfilePictureService
from app.core.identity.services.staff_service import StaffService
from app.core.shared.schemas.enums import ExportFormat, StaffAvailability, ArchiveReason
from app.core.identity.schemas.staff import (
    StaffCreate,
    StaffUpdate,
    StaffResponse,
    StaffFilterParams,
    StaffAudit,
)
from fastapi import Depends, APIRouter
from app.core.shared.schemas.shared_models import ArchiveRequest, UploadResponse
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import (
    get_authenticated_factory,
    get_authenticated_service,
)
from app.core.shared.services.file_storage.s3_upload import S3Upload

token_service = TokenService()
access = AccessTokenBearer()
router = APIRouter()


# Archive routers


@router.get("/archive/staff", response_model=List[StaffResponse])
def get_archived_staff(
    filters: StaffFilterParams = Depends(),
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    return factory.get_all_archived_staff(filters)


@router.get("/archive/staff/{staff_id}/audit", response_model=StaffAudit)
def get_archived_staff_audit(
    staff_id: UUID,
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    return factory.get_archived_staff(staff_id)


@router.get("/archive/staff/{staff_id}", response_model=StaffResponse)
def get_archived_staff(
    staff_id: UUID,
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    return factory.get_archived_staff(staff_id)


@router.patch("/archive/staff/{staff_id}", response_model=StaffResponse)
def restore_staff(
    staff_id: UUID,
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    return factory.restore_staff(staff_id)


@router.delete("/archive/staff/{staff_id}", status_code=204)
def delete_archived_staff(
    staff_id: UUID,
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    return factory.delete_archived_staff(staff_id)


# Active routers


@router.post("/staff", response_model=StaffResponse, status_code=201)
def create_staff(
    payload: StaffCreate,
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    return factory.create_staff(payload)


@router.post(
    "/staff/{staff_id}/profile/profile-picture",
    response_model=UploadResponse,
    status_code=201,
)
def upload_profile_pic(
    staff_id: UUID,
    file: UploadFile = File(...),
    service: ProfilePictureService = Depends(
        get_authenticated_service(ProfilePictureService)
    ),
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    staff = factory.get_staff(staff_id)
    result = service.upload_profile_picture(file, staff)

    return UploadResponse(**result)


@router.get("/staff/{staff_id}/profile/profile-picture")
def get_staff_profile_pic(
    staff_id: UUID,
    service: S3Upload = Depends(get_authenticated_service(S3Upload)),
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    staff = factory.get_staff(staff_id)
    key = staff.profile_s3_key
    return service.generate_presigned_url(key)


@router.delete("/staff/{staff_id}/profile/profile-picture", status_code=204)
def remove_profile_pic(
    staff_id: UUID,
    service: ProfilePictureService = Depends(
        get_authenticated_service(ProfilePictureService)
    ),
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    staff = factory.get_staff(staff_id)
    return service.remove_profile_pic(staff)


@router.post("/staff/", response_model=StaffResponse, status_code=201)
def create_staff(
    payload: StaffCreate,
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    return factory.create_staff(payload)


@router.get(
    "/staff/{staff_id}/profile/permissions-change-history",
    response_model=List[RoleHistoryResponse],
)
def get_staff_role_history(
    staff_id: UUID,
    filters: RoleHistoryFilterParams = Depends(),
    factory: RoleHistoryFactory = Depends(
        get_authenticated_factory(RoleHistoryFactory)
    ),
):
    filters.staff_id = staff_id
    return factory.get_all_history(filters)


@router.get("/staff/", response_model=List[StaffResponse])
def get_staff(
    filters: StaffFilterParams = Depends(),
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    return factory.get_all_staff(filters)


@router.get("/staff/{staff_id}/audit", response_model=StaffAudit)
def get_staff_audit(
    staff_id: UUID,
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    return factory.get_staff(staff_id)


@router.get("/staff/{staff_id}", response_model=StaffResponse)
def get_staff(
    staff_id: UUID,
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    return factory.get_staff(staff_id)


@router.put("/staff/{staff_id}", response_model=StaffResponse)
def update_staff(
    payload: StaffUpdate,
    staff_id: UUID,
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    payload = payload.model_dump(exclude_unset=True)
    return factory.update_staff(staff_id, payload)


@router.patch("/staff/{staff_id}/archive", status_code=204)
def archive_staff(
    staff_id: UUID,
    reason: ArchiveRequest,
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    return factory.archive_staff(staff_id, reason.reason)


@router.patch("/staff/{staff_id}/deep_archive", status_code=204)
def cascade_archive_staff(
    staff_id: UUID,
    reason: ArchiveReason,
    service: StaffService = Depends(get_authenticated_service(StaffService)),
):
    return service.cascade_staff_archive(staff_id, reason.value)


@router.patch("/{staff_id}/permissions", response_model=RoleHistoryResponse)
def change_staff_role(
    staff_id: UUID,
    payload: RoleHistoryCreate,
    factory: RoleHistoryFactory = Depends(
        get_authenticated_factory(RoleHistoryFactory)
    ),
):
    return factory.create_history(staff_id, payload)


@router.patch("/{staff_id}/role/assign", response_model=StaffResponse)
def assign_staff_role(
    staff_id: UUID,
    role_id: UUID,
    service: StaffService = Depends(get_authenticated_service(StaffService)),
):
    return service.assign_role(staff_id, role_id)


@router.patch("/{staff_id}/role/remove", response_model=StaffResponse)
def remove_staff_role(
    staff_id: UUID,
    service: StaffService = Depends(get_authenticated_service(StaffService)),
):
    return service.assign_role(staff_id)


@router.patch("/{staff_id}/department/assign", response_model=StaffResponse)
def assign_staff_department(
    staff_id: UUID,
    role_id: UUID,
    service: StaffService = Depends(get_authenticated_service(StaffService)),
):
    return service.assign_department(staff_id, role_id)


@router.patch("/{staff_id}/department/remove", response_model=StaffResponse)
def remove_staff_department(
    staff_id: UUID,
    service: StaffService = Depends(get_authenticated_service(StaffService)),
):
    return service.assign_department(staff_id)


@router.patch("/{staff_id}/availability", response_model=StaffResponse)
def change_staff_availability(
    staff_id: UUID,
    availability: StaffAvailability,
    service: StaffService = Depends(get_authenticated_service(StaffService)),
):
    return service.update_staff_availability(staff_id, availability)


@router.patch("/{staff_id}", status_code=204)
def archive_staff(
    staff_id: UUID,
    reason: ArchiveRequest,
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    return factory.archive_staff(staff_id, reason.reason)


@router.post("/{staff_id}", response_class=FileResponse, status_code=204)
def export_staff(
    staff_id: UUID,
    export_format: ExportFormat,
    service: StaffService = Depends(get_authenticated_service(StaffService)),
):
    file_path = service.export_staff(staff_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream",
    )


@router.delete("/{staff_id}", status_code=204)
def delete_staff(
    staff_id: UUID,
    factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
):
    return factory.delete_staff(staff_id)
