from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.responses import FileResponse
from fastapi import Depends, APIRouter
from fastapi import Query
from typing import Annotated

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.identity.schemas.guardian import GuardianCreate, GuardianUpdate, GuardianResponse, GuardianFilterParams
from V2.app.core.shared.database.session_manager import get_db
from V2.app.core.identity.crud.guardian import GuardianCrud
from V2.app.core.shared.schemas.shared_models import ArchiveRequest


router = APIRouter()


@router.post("/", response_model= GuardianResponse, status_code=201)
def create_guardian(data:GuardianCreate,
                db: Session = Depends(get_db)):
        guardian_crud = GuardianCrud(db)
        return guardian_crud.create_guardian(data)


@router.get("/", response_model=list[GuardianResponse])
def get_guardians(filters: Annotated[GuardianFilterParams, Query()],
                db: Session = Depends(get_db)):
        guardian_crud = GuardianCrud(db)
        return guardian_crud.get_all_guardians(filters)


@router.get("/{guardian_id}", response_model=GuardianResponse)
def get_guardian(guardian_id: UUID, db: Session = Depends(get_db)):
        guardian_crud = GuardianCrud(db)
        return guardian_crud.get_guardian(guardian_id)


@router.put("/{guardian_id}", response_model=GuardianResponse)
def update_guardian(data: GuardianUpdate, guardian_id: UUID,
                         db: Session = Depends(get_db)):
        guardian_crud = GuardianCrud(db)
        return guardian_crud.update_guardian(guardian_id, data)


@router.patch("/{guardian_id}", status_code=204)
def archive_guardian(guardian_id: UUID, reason:ArchiveRequest,
                          db: Session = Depends(get_db)):
        guardian_crud = GuardianCrud(db)
        return guardian_crud.archive_guardian(guardian_id, reason.reason)


@router.post("/{guardian_id}", response_class=FileResponse,  status_code=204)
def export_guardian(guardian_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    guardian_crud = GuardianCrud(db)
    file_path= guardian_crud.export_guardian(guardian_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{guardian_id}", status_code=204)
def delete_guardian(guardian_id: UUID, db: Session = Depends(get_db)):
        guardian_crud = GuardianCrud(db)
        return guardian_crud.delete_guardian(guardian_id)











