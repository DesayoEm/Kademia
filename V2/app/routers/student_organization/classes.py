from sqlalchemy.orm import Session
from uuid import UUID
from ...schemas.student_organization.classes import(
    ClassCreate, ClassUpdate, ClassFilterParams, ClassResponse
)
from ...schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from ...database.session_manager import get_db
from ...crud.student_organization.classes import ClassCrud
from fastapi import Query
from typing import Annotated

router = APIRouter()

@router.post("/", response_model= ClassResponse, status_code=201)
def create_class(data:ClassCreate,
                            db: Session = Depends(get_db)):
    class_crud = ClassCrud(db)
    return class_crud.create_class(data)

@router.get("/", response_model=list[ClassResponse])
def get_classes(filters: Annotated[ClassFilterParams, Query()],
                          db: Session = Depends(get_db)):
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


@router.delete("/{class_id}", status_code=204)
def delete_class(class_id: UUID, db: Session = Depends(get_db)):
    class_crud = ClassCrud(db)
    return class_crud.delete_class(class_id)










