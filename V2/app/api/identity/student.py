
from uuid import UUID
from typing import List
from fastapi import Depends, APIRouter
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.identity.schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentFilterParams
from V2.app.core.identity.crud.student import StudentCrud
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()


@router.post("/", response_model= StudentResponse, status_code=201)
def create_student(
        data:StudentCreate,
        crud: StudentCrud = Depends(get_authenticated_crud(StudentCrud))
    ):
        return crud.create_student(data)


@router.get("/", response_model=List[StudentResponse])
def get_students(
        filters: StudentFilterParams = Depends(),
        crud: StudentCrud = Depends(get_authenticated_crud(StudentCrud))
    ):
        return crud.get_all_students(filters)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
        student_id: UUID,
        crud: StudentCrud = Depends(get_authenticated_crud(StudentCrud))
    ):
        return crud.get_student(student_id)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
        data: StudentUpdate,
        student_id: UUID,
        crud: StudentCrud = Depends(get_authenticated_crud(StudentCrud))
    ):
        return crud.update_student(student_id, data)


@router.patch("/{student_id}", status_code=204)
def archive_student(
        student_id: UUID,
        reason:ArchiveRequest,
        crud: StudentCrud = Depends(get_authenticated_crud(StudentCrud))
    ):
        return crud.archive_student(student_id, reason.reason)


@router.post("/{student_id}", response_class=FileResponse,  status_code=204)
def export_student(
        student_id: UUID,
        export_format: ExportFormat,
        crud: StudentCrud = Depends(get_authenticated_crud(StudentCrud))
    ):
    file_path= crud.export_student(student_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{student_id}", status_code=204)
def delete_student(
        student_id: UUID,
        crud: StudentCrud = Depends(get_authenticated_crud(StudentCrud))
    ):
        return crud.delete_student(student_id)











