
from uuid import UUID
from typing import List, Annotated
from fastapi.responses import FileResponse
from fastapi import UploadFile, File
from V2.app.core.identity.factories.staff import StaffFactory
from V2.app.core.identity.services import IdentityService
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.identity.schemas.staff import StaffCreate, StaffUpdate, StaffResponse, StaffFilterParams
from fastapi import Depends, APIRouter
from V2.app.core.shared.schemas.shared_models import ArchiveRequest, UploadResponse
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()

@router.post("/", response_model= StaffResponse, status_code=201)
def create_staff(
        payload:StaffCreate,
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
    ):
        return factory.create_staff(payload)


@router.post("/{staff_id}/profile/upload-profile-pic", response_model= UploadResponse,
             status_code=201)
def upload_profile_pic(
        staff_id: UUID,
        file: UploadFile = File(...),
        service: IdentityService = Depends(get_authenticated_service(IdentityService)),
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory))
    ):
        staff = factory.get_staff(staff_id)
        result = service.upload_profile_picture(file, staff)

        return UploadResponse(**result)


@router.post("/", response_model= StaffResponse, status_code=201)
def create_staff(
        payload:StaffCreate,
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory)),
    ):
        return factory.create_staff(payload)


@router.get("/", response_model=List[StaffResponse])
def get_staff(
        filters: StaffFilterParams = Depends(),
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory))
    ):
        return factory.get_all_staff(filters)


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(
        staff_id: UUID,
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory))
    ):
        return factory.get_staff(staff_id)


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(
        payload: StaffUpdate,
        staff_id: UUID,
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory))
    ):  
        
        return factory.update_staff(staff_id, payload)


@router.patch("/{staff_id}", status_code=204)
def archive_staff(
        staff_id: UUID,
        reason:ArchiveRequest,
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory))
    ):
        return factory.archive_staff(staff_id, reason.reason)


@router.post("/{staff_id}", response_class=FileResponse,  status_code=204)
def export_staff(
        staff_id: UUID,
        export_format: ExportFormat,
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory))
    ):
    file_path= factory.export_staff(staff_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{staff_id}", status_code=204)
def delete_staff(
        staff_id: UUID,
        factory: StaffFactory = Depends(get_authenticated_factory(StaffFactory))
    ):
        return factory.delete_staff(staff_id)











