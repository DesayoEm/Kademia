
from uuid import UUID
from typing import List
from fastapi.responses import FileResponse

from V2.app.core.shared.schemas.enums import ExportFormat
from V2.app.core.shared.schemas.shared_models import ArchiveRequest
from fastapi import Depends, APIRouter
from V2.app.core.curriculum.crud.subject_educator import SubjectEducatorCrud
from V2.app.core.curriculum.schemas.subject_educator import(
    SubjectEducatorCreate, SubjectEducatorFilterParams, SubjectEducatorResponse
)
from V2.app.core.auth.services.token_service import TokenService
from V2.app.core.auth.services.dependencies.token_deps import AccessTokenBearer
from V2.app.core.auth.services.dependencies.current_user_deps import get_authenticated_crud

token_service=TokenService()
access = AccessTokenBearer()
router = APIRouter()



@router.post("/{educator_id}", response_model= SubjectEducatorResponse, status_code=201)
def assign_subject_educator(
        educator_id: UUID,
        data:SubjectEducatorCreate,
        crud: SubjectEducatorCrud = Depends(get_authenticated_crud(SubjectEducatorCrud))
    ):
    return crud.create_subject_educator(educator_id,data)


@router.get("/", response_model=List[SubjectEducatorResponse])
def get_subject_educators(
        filters: SubjectEducatorFilterParams = Depends(),
        crud: SubjectEducatorCrud = Depends(get_authenticated_crud(SubjectEducatorCrud))
    ):
    return crud.get_all_subject_educators(filters)


@router.get("/{subject_educator_id}", response_model=SubjectEducatorResponse)
def get_subject_educator(
        subject_educator_id: UUID,
        crud: SubjectEducatorCrud = Depends(get_authenticated_crud(SubjectEducatorCrud))
    ):
    return crud.get_subject_educator(subject_educator_id)


@router.patch("/{subject_educator_id}",  status_code=204)
def archive_subject_educator(
        subject_educator_id: UUID,
        reason:ArchiveRequest,
        crud: SubjectEducatorCrud = Depends(get_authenticated_crud(SubjectEducatorCrud))
    ):
    return crud.archive_subject_educator(subject_educator_id, reason.reason)


@router.post("/{subject_educator_id}", response_class=FileResponse,  status_code=204)
def export_subject_educator(
        subject_educator_id: UUID,
        export_format: ExportFormat,
        crud: SubjectEducatorCrud = Depends(get_authenticated_crud(SubjectEducatorCrud))
    ):
    file_path= crud.export_subject_educator(subject_educator_id, export_format.value)

    return FileResponse(
        path=file_path,
        filename=file_path.split("/")[-1],
        media_type="application/octet-stream"
    )


@router.delete("/{subject_educator_id}", status_code=204)
def delete_subject_educator(
        subject_educator_id: UUID,
        crud: SubjectEducatorCrud = Depends(get_authenticated_crud(SubjectEducatorCrud))
    ):
    return crud.delete_subject_educator(subject_educator_id)










