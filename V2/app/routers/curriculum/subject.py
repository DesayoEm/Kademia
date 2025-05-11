from uuid import UUID
from typing import List
from fastapi.responses import FileResponse
from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.core.curriculum.crud.subject import SubjectCrud
from V2.app.core.curriculum.schemas.subject import(
    SubjectCreate, SubjectUpdate, SubjectFilterParams, SubjectResponse
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("/", response_model= SubjectResponse, status_code=201)
def create_subject(
        data:SubjectCreate,
        crud: SubjectCrud = Depends(get_authenticated_crud(SubjectCrud))
    ):
    return crud.create_subject(data)


@router.get("/", response_model=List[SubjectResponse])
def get_subjects(
        filters: SubjectFilterParams = Depends(),
        crud: SubjectCrud = Depends(get_authenticated_crud(SubjectCrud))
    ):
    return crud.get_all_subjects(filters)


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(
        subject_id: UUID,
        crud: SubjectCrud = Depends(get_authenticated_crud(SubjectCrud))
    ):
    return crud.get_subject(subject_id)


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
        data: SubjectUpdate,
        subject_id: UUID,
        crud: SubjectCrud = Depends(get_authenticated_crud(SubjectCrud))
    ):
    return crud.update_subject(subject_id, data)


@router.patch("/{subject_id}",  status_code=204)
def archive_subject(
        subject_id: UUID,
        reason:ArchiveRequest,
        crud: SubjectCrud = Depends(get_authenticated_crud(SubjectCrud))
    ):
    return crud.archive_subject(subject_id, reason.reason)


@router.post("/{subject_id}", response_class=FileResponse,  status_code=204)
def export_subject(
        subject_id: UUID,
        export_format: ExportFormat,
        crud: SubjectCrud = Depends(get_authenticated_crud(SubjectCrud))
    ):
    file_path= crud.export_subject(subject_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{subject_id}", status_code=204)
def delete_subject(
        subject_id: UUID,
        crud: SubjectCrud = Depends(get_authenticated_crud(SubjectCrud))
    ):
    return crud.delete_subject(subject_id)










