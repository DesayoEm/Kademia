from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.infra.db.session_manager import get_db
from V2.app.core.academic_structure.crud.classes import ClassCrud
from V2.app.core.academic_structure.schemas.classes import(
    ClassCreate, ClassUpdate, ClassFilterParams, ClassResponse
)

router = APIRouter()

@router.post("/", response_model= ClassResponse, status_code=201)
def create_class(data:ClassCreate,
                            db: Session = Depends(get_db)):
    class_crud = ClassCrud(db)
    return class_crud.create_class(data)

@router.get("/", response_model=list[ClassResponse])
def get_classes(filters: ClassFilterParams = Depends(),db: Session = Depends(get_db)):
    class_crud = ClassCrud(db)
    return class_crud.get_all_classes(filters)

@router.get("/{class_id}", response_model=ClassResponse)
def get_class(class_id: UUID, db: Session = Depends(get_db)):
    class_crud = ClassCrud(db)
    return class_crud.get_class(class_id)

@router.put("/{class_id}", response_model=ClassResponse)
def update_class(data: ClassUpdate, class_id: UUID,
                            db: Session = Depends(get_db)):
    class_crud = ClassCrud(db)
    return class_crud.update_class(class_id, data)

@router.patch("/{class_id}",  status_code=204)
def archive_class(class_id: UUID, reason:ArchiveRequest,
                       db: Session = Depends(get_db)):
    class_crud = ClassCrud(db)
    return class_crud.archive_class(class_id, reason.reason)


@router.post("/{class_id}", response_class=FileResponse,  status_code=204)
def export_class(class_id: UUID, export_format: ExportFormat, db: Session = Depends(get_db)):
    class_crud = ClassCrud(db)
    file_path= class_crud.export_class(class_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{class_id}", status_code=204)
def delete_class(class_id: UUID, db: Session = Depends(get_db)):
    class_crud = ClassCrud(db)
    return class_crud.delete_class(class_id)










