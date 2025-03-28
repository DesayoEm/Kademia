from sqlalchemy.orm import Session
from uuid import UUID
from ...schemas.student_organization.classes import ClassFilterParams, ClassResponse
from fastapi import Depends, APIRouter
from ...database.session import get_db
from ...crud.student_organization.classes import ClassCrud
from fastapi import Query
from typing import Annotated

router = APIRouter()

@router.get("/", response_model=list[ClassResponse])
def get_archived_classes(filters: Annotated[ClassFilterParams, Query()],
                             db: Session = Depends(get_db)):
    class_crud = ClassCrud(db)
    return class_crud.get_all_archived_classes(filters)


@router.get("/{class_id}", response_model=ClassResponse)
def get_archived_class(class_id: UUID, db: Session = Depends(get_db)):
    class_crud = ClassCrud(db)
    return class_crud.get_archived_class(class_id)


@router.patch("/{class_id}", response_model=ClassResponse)
def restore_class(class_id: UUID,db: Session = Depends(get_db)):
    class_crud = ClassCrud(db)
    return class_crud.restore_class(class_id)


@router.delete("/{class_id}", status_code=204)
def delete_archived_class(class_id: UUID, db: Session = Depends(get_db)):
    class_crud = ClassCrud(db)
    return class_crud.delete_archived_class(class_id)




