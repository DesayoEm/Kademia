
from uuid import UUID
from fastapi.responses import FileResponse

from fastapi import Depends, APIRouter
from app.core.shared.schemas.enums import ExportFormat
from app.core.staff_management.factories.qualification import QualificationFactory
from app.core.shared.schemas.shared_models import ArchiveRequest
from app.core.staff_management.schemas.qualification import(
    QualificationCreate, QualificationUpdate, QualificationResponse, QualificationFilterParams
)
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, get_authenticated_service
from app.core.staff_management.services.staff_management import StaffManagementService

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()

@router.get("/", response_model=list[QualificationResponse])
def get_archived_qualifications(
        filters: QualificationFilterParams = Depends(),
        factory: QualificationFactory = Depends(get_authenticated_factory(QualificationFactory))
    ):
    return factory.get_all_archived_qualifications(filters)


@router.get("/{qualification_id}", response_model=QualificationResponse)
def get_archived_qualification(
        qualification_id: UUID,
        factory: QualificationFactory = Depends(get_authenticated_factory(QualificationFactory))
    ):
    return factory.get_archived_qualification(qualification_id)


@router.patch("/{qualification_id}", response_model=QualificationResponse)
def restore_qualification(
        qualification_id: UUID,
        factory: QualificationFactory = Depends(get_authenticated_factory(QualificationFactory))
    ):
    return factory.restore_qualification(qualification_id)


@router.delete("/{qualification_id}", status_code=204)
def delete_archived_qualification(
        qualification_id: UUID,
        factory: QualificationFactory = Depends(get_authenticated_factory(QualificationFactory))
    ):
    return factory.delete_archived_qualification(qualification_id)



@router.post("/{educator_id}", response_model= QualificationResponse, status_code=201)
def add_qualification(
        educator_id: UUID,
        payload:QualificationCreate,
        factory: QualificationFactory = Depends(get_authenticated_factory(QualificationFactory))
    ):
        return factory.create_qualification(educator_id, payload)


@router.get("/", response_model=list[QualificationResponse])
def get_qualifications(
        filters: QualificationFilterParams = Depends(),
        factory: QualificationFactory = Depends(get_authenticated_factory(QualificationFactory))
    ):
        return factory.get_all_qualifications(filters)


@router.get("/{qualification_id}", response_model=QualificationResponse)
def get_qualification(
        qualification_id: UUID,
        factory: QualificationFactory = Depends(get_authenticated_factory(QualificationFactory))
    ):
        return factory.get_qualification(qualification_id)


@router.put("/{qualification_id}", response_model=QualificationResponse)
def update_qualification(
        payload: QualificationUpdate,
        qualification_id: UUID,
        factory: QualificationFactory = Depends(get_authenticated_factory(QualificationFactory))
    ):
        payload = payload.model_dump(exclude_unset=True)
        return factory.update_qualification(qualification_id, payload)


@router.patch("/{qualification_id}", status_code=204)
def archive_qualification(
        qualification_id: UUID,
        reason:ArchiveRequest,
    factory: QualificationFactory = Depends(get_authenticated_factory(QualificationFactory))
    ):
        return factory.archive_qualification(qualification_id, reason.reason)


@router.post("/{qualification_id}", response_class=FileResponse,  status_code=204)
def export_qualification(
        qualification_id: UUID,
        export_format: ExportFormat,
        service: StaffManagementService = Depends(get_authenticated_service(StaffManagementService))
    ):
    file_path= service.export_qualification_audit(qualification_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{qualification_id}", status_code=204)
def delete_qualification(
        qualification_id: UUID,
        factory: QualificationFactory = Depends(get_authenticated_factory(QualificationFactory))
    ):
        return factory.delete_qualification(qualification_id)











