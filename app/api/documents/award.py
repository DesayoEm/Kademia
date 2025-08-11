
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse
from fastapi import UploadFile, File


from app.core.documents.factories.award_factory import AwardFactory
from app.core.documents.services.document_service import DocumentService
from app.core.identity.factories.student import StudentFactory
from app.core.shared.schemas.enums import ExportFormat
from app.core.shared.schemas.shared_models import ArchiveRequest, UploadResponse
from fastapi import Depends, APIRouter
from app.core.documents.schemas.student_award import (
    AwardFilterParams, AwardCreate, AwardUpdate, AwardResponse, AwardAudit
)
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service
from app.core.shared.services.file_storage.s3_upload import S3Upload


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()

#Archive routers
@router.get("/archive/awards/", response_model=List[AwardResponse])
def get_archived_awards(
        filters: AwardFilterParams = Depends(),
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.get_all_archived_awards(filters)


@router.get("/archive/awards/{award_id}/audit", response_model=AwardAudit)
def get_archived_award_audit(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.get_archived_award(award_id)


@router.get("/archive/awards/{award_id}", response_model=AwardResponse)
def get_archived_award(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.get_archived_award(award_id)


@router.patch("/archive/awards/{award_id}", response_model=AwardResponse)
def restore_award(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.restore_award(award_id)


@router.delete("/archive/awards/{award_id}", status_code=204)
def delete_archived_award(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.delete_archived_award(award_id)



#Active routers
@router.post("/{student_id}/awards/{award_id}/file", response_model= UploadResponse,
             status_code=201)
def upload_award_file(
        award_id: UUID,
        student_id: UUID,
        file: UploadFile = File(...),
        service: DocumentService = Depends(get_authenticated_service(DocumentService)),
        award_factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory)),
        student_factory: StudentFactory = Depends(get_authenticated_factory(StudentFactory))
    ):
        award = award_factory.get_award(award_id)
        student = student_factory.get_student(student_id)
        result = service.upload_award_file(file, student, award)

        return UploadResponse(**result)


@router.get("/awards/{award_id}/file")
def get_award_file(
        award_id: UUID,
        service: S3Upload = Depends(get_authenticated_service(S3Upload)),
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
        award = factory.get_award(award_id)
        key = award.award_s3_key
        return service.generate_presigned_url(key)


@router.delete("/awards/{award_id}/file", status_code=204)
def remove_award_file(
        award_id: UUID,
        service: DocumentService = Depends(get_authenticated_service(DocumentService)),
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
        award = factory.get_award(award_id)
        return service.remove_award_file(award)


@router.post("{student_id}/", response_model= AwardResponse, status_code=201)
def create_award(
        student_id: UUID,
        payload:AwardCreate,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.create_award(student_id, payload)


@router.get("/awards/", response_model=List[AwardResponse])
def get_awards(
        filters: AwardFilterParams = Depends(),
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.get_all_awards(filters)


@router.get("/awards/{award_id}/audit", response_model=AwardAudit)
def get_award_audit(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
     ):
    return factory.get_award(award_id)


@router.get("/awards/{award_id}", response_model=AwardResponse)
def get_award(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
     ):
    return factory.get_award(award_id)


@router.put("/awards/{award_id}", response_model=AwardResponse)
def update_award(
        payload: AwardUpdate,
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    payload = payload.model_dump(exclude_unset=True)
    return factory.update_award(award_id, payload)


@router.patch("/awards/{award_id}",  status_code=204)
def archive_award(
        award_id: UUID,
        reason:ArchiveRequest,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
    ):
    return factory.archive_award(award_id, reason.reason)


@router.post("/awards/{award_id}/audit", response_class=FileResponse,  status_code=204)
def export_award_audit(
        award_id: UUID,
        export_format: ExportFormat,
        service: DocumentService = Depends(get_authenticated_service(DocumentService))
):
    file_path= service.export_award_audit(award_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/awards/{award_id}", status_code=204)
def delete_award(
        award_id: UUID,
        factory: AwardFactory = Depends(get_authenticated_factory(AwardFactory))
):
    return factory.delete_award(award_id)










