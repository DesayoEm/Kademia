
from uuid import UUID
from fastapi.responses import FileResponse

from app.core.identity.services.staff_service import StaffService
from app.core.shared.schemas.enums import ExportFormat
from app.core.identity.schemas.staff import  StaffResponse
from fastapi import Depends, APIRouter
from app.core.auth.services.token_service import TokenService
from app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from app.core.auth.services.dependencies.current_user_deps import get_authenticated_factory, \
    get_authenticated_service


token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("/{staff_id}", response_class=FileResponse,  status_code=204)
def export_staff(
        staff_id: UUID,
        export_format: ExportFormat,
        service: StaffService = Depends(get_authenticated_service(StaffService)),
    ):
    file_path= service.export_staff(staff_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )














