from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.identity.schemas.staff import StaffCreate, StaffUpdate, StaffResponse, StaffFilterParams
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.identity.crud.staff import StaffCrud
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer


router = APIRouter()
bearer= AccessTokenBearer()

@router.post("/", response_model= StaffResponse, status_code=201)
def create_staff(data:StaffCreate,db: Session = Depends(get_db),
                        ):
        staff_crud = StaffCrud(db)
        return staff_crud.create_staff(data)


@router.get("/", response_model=list[StaffResponse])
def get_staff(filters: StaffFilterParams = Depends(),db: Session = Depends(get_db)):
        staff_crud = StaffCrud(db)
        return staff_crud.get_all_staff(filters)


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: UUID, db: Session = Depends(get_db)):
        staff_crud = StaffCrud(db)
        return staff_crud.get_staff(staff_id)


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(data: StaffUpdate, staff_id: UUID,
                         db: Session = Depends(get_db)):
        staff_crud = StaffCrud(db)
        return staff_crud.update_staff(staff_id, data)


@router.patch("/{staff_id}", status_code=204)
def archive_staff(staff_id: UUID, reason:ArchiveRequest,
                          db: Session = Depends(get_db)):
        staff_crud = StaffCrud(db)
        return staff_crud.archive_staff(staff_id, reason.reason)


@router.post("/{staff_id}", response_class=FileResponse,  status_code=204)
def export_staff(staff_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    staff_crud = StaffCrud(db)
    file_path= staff_crud.export_staff(staff_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )

@router.delete("/{staff_id}", status_code=204)
def delete_staff(staff_id: UUID, db: Session = Depends(get_db)):
        staff_crud = StaffCrud(db)
        return staff_crud.delete_staff(staff_id)











