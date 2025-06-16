
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse
from fastapi import Depends, APIRouter, UploadFile, File
from V2.app.core.shared.services.file_storage.s3_upload import S3Upload
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.identity.schemas.guardian import (
    GuardianCreate, GuardianUpdate, GuardianResponse, GuardianFilterParams, GuardianAudit
)

from V2.app.core.identity.factories.guardian import GuardianFactory
from V2.app.core.identity.services.profile_picture_service import ProfilePictureService
from V2.app.core.identity.services.gaurdian_service import GuardianService
from V2.app.core.shared.schemas.shared_models import ArchiveRequest, UploadResponse
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory,\
    get_authenticated_service 


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("/", response_model= GuardianResponse, status_code=201)
def create_guardian(
        payload:GuardianCreate,
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
        return factory.create_guardian(payload)


@router.post("/{guardian_id}/profile/profile-picture", response_model= UploadResponse,
             status_code=201)
def upload_profile_pic(
        guardian_id: UUID,
        file: UploadFile = File(...),
        service: ProfilePictureService = Depends(get_authenticated_service(ProfilePictureService)),
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
        guardian = factory.get_guardian(guardian_id)
        result = service.upload_profile_picture(file, guardian)

        return UploadResponse(**result)


@router.get("/{guardian_id}/profile/profile-picture")
def get_guardian_profile_pic(
        guardian_id: UUID,
        service: S3Upload = Depends(get_authenticated_service(S3Upload)),
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
        guardian = factory.get_guardian(guardian_id)
        key = guardian.profile_s3_key
        return service.generate_presigned_url(key)


@router.delete("/{guardian_id}/profile/profile-picture", status_code=204)
def remove_profile_pic(
        guardian_id: UUID,
        service: ProfilePictureService = Depends(get_authenticated_service(ProfilePictureService)),
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
        guardian = factory.get_guardian(guardian_id)
        return service.remove_profile_pic(guardian)


@router.get("/", response_model=List[GuardianResponse])
def get_guardians(
        filters: GuardianFilterParams = Depends(),
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
        return factory.get_all_guardians(filters)


@router.get("/{guardian_id}/audit", response_model=GuardianAudit)
def get_guardian_audit(
        guardian_id: UUID,
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
        return factory.get_guardian(guardian_id)


@router.get("/{guardian_id}", response_model=GuardianResponse)
def get_guardian(
        guardian_id: UUID, 
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
        return factory.get_guardian(guardian_id)


@router.put("/{guardian_id}", response_model=GuardianResponse)
def update_guardian(
        payload: GuardianUpdate, 
        guardian_id: UUID,
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
        payload = payload.model_dump(exclude_unset=True)
        return factory.update_guardian(guardian_id, payload)


@router.patch("/{guardian_id}", status_code=204)
def archive_guardian(
        guardian_id: UUID, 
        reason:ArchiveRequest,
        factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
        return factory.archive_guardian(guardian_id, reason.reason)


@router.post("/{guardian_id}", response_class=FileResponse,  status_code=204)
def export_guardian(
        guardian_id: UUID, 
        export_format: ExportFormat, 
        service: GuardianService = Depends(get_authenticated_service(GuardianService)),
    ):
    file_path= service.export_guardian(guardian_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{guardian_id}", status_code=204)
def delete_guardian(
        guardian_id: UUID, factory: GuardianFactory = Depends(get_authenticated_factory(GuardianFactory)),
    ):
        return factory.delete_guardian(guardian_id)











